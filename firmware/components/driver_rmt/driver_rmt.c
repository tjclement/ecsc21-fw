#include <sdkconfig.h>

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include <esp_log.h>
#include <driver/i2c.h>
#include <driver/rmt.h>

#include "include/driver_rmt.h"

#define RMT_RX_ACTIVE_LEVEL 0 /*!< If we connect with a IR receiver, the data is active low */
#define RMT_TX_CARRIER_EN   1 /*!< Enable carrier for IR transmitter test with IR led */

#define RMT_TX_CHANNEL  1                     /*!< RMT channel for transmitter */
#define RMT_TX_GPIO_NUM CONFIG_PIN_NUM_RMT_TX /*!< GPIO number for transmitter signal */
#define RMT_RX_CHANNEL  0                     /*!< RMT channel for receiver */
#define RMT_RX_GPIO_NUM CONFIG_PIN_NUM_RMT_RX /*!< GPIO number for receiver */
#define RMT_CLK_DIV     80                    /*!< RMT counter clock divider */
#define RMT_TICK_1_US   1                     /*!< RMT counter value for 1 us.(Source clock is APB clock)*/

#define NEC_HEADER_HIGH_US  9000 /*!< NEC protocol header: positive 9ms */
#define NEC_HEADER_LOW_US   4500 /*!< NEC protocol header: negative 4.5ms*/
#define NEC_BIT_ONE_HIGH_US 560  /*!< NEC protocol data bit 1: positive 0.56ms */
#define NEC_BIT_ONE_LOW_US \
  (2250 - NEC_BIT_ONE_HIGH_US)   /*!< NEC protocol data bit 1: negative 1.69ms */
#define NEC_BIT_ZERO_HIGH_US 560 /*!< NEC protocol data bit 0: positive 0.56ms */
#define NEC_BIT_ZERO_LOW_US \
  (1120 - NEC_BIT_ZERO_HIGH_US) /*!< NEC protocol data bit 0: negative 0.56ms */
#define NEC_BIT_END    560      /*!< NEC protocol end: positive 0.56ms */
#define NEC_BIT_MARGIN 80       /*!< NEC parse margin time */

#define NEC_ITEM_DURATION(d) \
  ((d & 0x7fff) * RMT_TICK_1_US) /*!< Parse duration time from memory register value */
#define NEC_DATA_ITEM_NUM     34       /*!< NEC code item number: header + 32bit data + end */
#define RMT_TX_DATA_NUM       10      /*!< NEC tx test data number */
#define RMT_TIMEOUT_US 9500            /*!< RMT receiver timeout value(us) */

#ifdef CONFIG_DRIVER_RMT_ENABLE

static const char *TAG                                            = "driver_rmt";
static void (*nec_rx_handler)(uint8_t, uint8_t, uint8_t, uint8_t) = NULL;

/*
 * @brief Build register value of waveform for NEC one data bit
 */
static inline void nec_fill_item_level(rmt_item32_t *item, int high_us, int low_us) {
  item->level0    = 1;
  item->duration0 = (high_us) * RMT_TICK_1_US;
  item->level1    = 0;
  item->duration1 = (low_us) * RMT_TICK_1_US;
}

/*
 * @brief Generate NEC header value: active 9ms + negative 4.5ms
 */
static void nec_fill_item_header(rmt_item32_t *item) {
  nec_fill_item_level(item, NEC_HEADER_HIGH_US, NEC_HEADER_LOW_US);
}

/*
 * @brief Generate NEC data bit 1: positive 0.56ms + negative 1.69ms
 */
static void nec_fill_item_bit_one(rmt_item32_t *item) {
  nec_fill_item_level(item, NEC_BIT_ONE_HIGH_US, NEC_BIT_ONE_LOW_US);
}

/*
 * @brief Generate NEC data bit 0: positive 0.56ms + negative 0.56ms
 */
static void nec_fill_item_bit_zero(rmt_item32_t *item) {
  nec_fill_item_level(item, NEC_BIT_ZERO_HIGH_US, NEC_BIT_ZERO_LOW_US);
}

/*
 * @brief Generate NEC end signal: positive 0.56ms
 */
static void nec_fill_item_end(rmt_item32_t *item) {
  nec_fill_item_level(item, NEC_BIT_END, 0x7fff);
}

/*
 * @brief Check whether duration is around target_us
 */
inline bool nec_check_in_range(int duration_ticks, int target_us, int margin_us) {
  if ((NEC_ITEM_DURATION(duration_ticks) < (target_us + margin_us)) &&
      (NEC_ITEM_DURATION(duration_ticks) > (target_us - margin_us))) {
    return true;
  } else {
    return false;
  }
}

/*
 * @brief Check whether this value represents an NEC header
 */
static bool nec_header_if(rmt_item32_t *item) {
  if ((item->level0 == RMT_RX_ACTIVE_LEVEL && item->level1 != RMT_RX_ACTIVE_LEVEL) &&
      nec_check_in_range(item->duration0, NEC_HEADER_HIGH_US, NEC_BIT_MARGIN) &&
      nec_check_in_range(item->duration1, NEC_HEADER_LOW_US, NEC_BIT_MARGIN)) {
    return true;
  }
  return false;
}

/*
 * @brief Check whether this value represents an NEC data bit 1
 */
static bool nec_bit_one_if(rmt_item32_t *item) {
  if ((item->level0 == RMT_RX_ACTIVE_LEVEL && item->level1 != RMT_RX_ACTIVE_LEVEL) &&
      nec_check_in_range(item->duration0, NEC_BIT_ONE_HIGH_US, NEC_BIT_MARGIN) &&
      nec_check_in_range(item->duration1, NEC_BIT_ONE_LOW_US, NEC_BIT_MARGIN)) {
    return true;
  }
  return false;
}

/*
 * @brief Check whether this value represents an NEC data bit 0
 */
static bool nec_bit_zero_if(rmt_item32_t *item) {
  if ((item->level0 == RMT_RX_ACTIVE_LEVEL && item->level1 != RMT_RX_ACTIVE_LEVEL) &&
      nec_check_in_range(item->duration0, NEC_BIT_ZERO_HIGH_US, NEC_BIT_MARGIN) &&
      nec_check_in_range(item->duration1, NEC_BIT_ZERO_LOW_US, NEC_BIT_MARGIN)) {
    return true;
  }
  return false;
}

/*
 * @brief Build NEC 32bit waveform.
 */
static int nec_build_items(int channel, rmt_item32_t *item, int item_num, uint16_t addr,
                           uint16_t cmd_data) {
  int i = 0, j = 0;
  if (item_num < NEC_DATA_ITEM_NUM) {
    return -1;
  }
  nec_fill_item_header(item++);
  i++;
  for (j = 0; j < 16; j++) {
    if (addr & 0x1) {
      nec_fill_item_bit_one(item);
    } else {
      nec_fill_item_bit_zero(item);
    }
    item++;
    i++;
    addr >>= 1;
  }
  for (j = 0; j < 16; j++) {
    if (cmd_data & 0x1) {
      nec_fill_item_bit_one(item);
    } else {
      nec_fill_item_bit_zero(item);
    }
    item++;
    i++;
    cmd_data >>= 1;
  }
  nec_fill_item_end(item);
  i++;
  return i;
}

/*
 * @brief Parse NEC 32 bit waveform to address and command.
 */
static int nec_parse_items(rmt_item32_t *item, int item_num, uint16_t *addr, uint16_t *data) {
  int w_len = item_num;
  if (w_len < NEC_DATA_ITEM_NUM) {
    ESP_LOGI(TAG, "RMT PAR --- w_len %d", w_len);
    return -1;
  }
  int i = 0, j = 0;
  if (!nec_header_if(item++)) {
    ESP_LOGI(TAG, "RMT PAR --- not nec header: %d | %d", item[-1].duration0, item[-1].duration1);
    return -1;
  }
  uint16_t addr_t = 0;
  for (j = 0; j < 16; j++) {
    if (nec_bit_one_if(item)) {
      addr_t |= (1 << j);
    } else if (nec_bit_zero_if(item)) {
      addr_t |= (0 << j);
    } else {
      ESP_LOGI(TAG, "RMT PAR --- addr 1 nor 0: %d | %d", item[-1].duration0, item[-1].duration1);
      return -1;
    }
    item++;
    i++;
  }
  uint16_t data_t = 0;
  for (j = 0; j < 16; j++) {
    if (nec_bit_one_if(item)) {
      data_t |= (1 << j);
    } else if (nec_bit_zero_if(item)) {
      data_t |= (0 << j);
    } else {
    ESP_LOGI(TAG, "RMT PAR --- data 1 nor 0: %d | %d", item[-1].duration0, item[-1].duration1);
      return -1;
    }
    item++;
    i++;
  }
  *addr = addr_t;
  *data = data_t;
  return i;
}

/*
 * @brief RMT transmitter initialization
 */
static void nec_tx_init() {
  rmt_config_t rmt_tx;
  rmt_tx.channel                        = RMT_TX_CHANNEL;
  rmt_tx.gpio_num                       = RMT_TX_GPIO_NUM;
  rmt_tx.mem_block_num                  = 1;
  rmt_tx.clk_div                        = RMT_CLK_DIV;
  rmt_tx.tx_config.loop_en              = false;
  rmt_tx.tx_config.carrier_duty_percent = 50;
  rmt_tx.tx_config.carrier_freq_hz      = 40000;
  rmt_tx.tx_config.carrier_level        = 1;
  rmt_tx.tx_config.carrier_en           = RMT_TX_CARRIER_EN;
  rmt_tx.tx_config.idle_level           = 0;
  rmt_tx.tx_config.idle_output_en       = true;
  rmt_tx.rmt_mode                       = 0;
  rmt_config(&rmt_tx);
  rmt_driver_install(rmt_tx.channel, 0, 0);
}

/*
 * @brief RMT receiver initialization
 */
static void nec_rx_init() {
  rmt_config_t rmt_rx;
  rmt_rx.channel                       = RMT_RX_CHANNEL;
  rmt_rx.gpio_num                      = RMT_RX_GPIO_NUM;
  rmt_rx.clk_div                       = RMT_CLK_DIV;
  rmt_rx.mem_block_num                 = 1;
  rmt_rx.rmt_mode                      = RMT_MODE_RX;
  rmt_rx.rx_config.filter_en           = true;
  rmt_rx.rx_config.filter_ticks_thresh = 500;
  rmt_rx.rx_config.idle_threshold      = RMT_TIMEOUT_US * (RMT_TICK_1_US);
  rmt_config(&rmt_rx);
  rmt_driver_install(rmt_rx.channel, 1000, 0);
}

/**
 * @brief RMT receiver demo, this task will print each received NEC data.
 *
 */
static void nec_rx_task() {
  int channel        = RMT_RX_CHANNEL;
  RingbufHandle_t rb = NULL;
  // get RMT RX ringbuffer
  rmt_get_ringbuf_handle(channel, &rb);
  while (rb) {
    size_t rx_size = 0;
    // try to receive data from ringbuffer.
    // RMT driver will push all the data it receives to its ringbuffer.
    // We just need to parse the value and return the spaces of ringbuffer.
    rmt_item32_t *item = (rmt_item32_t *)xRingbufferReceive(rb, &rx_size, 1000);

    if (item) {
//      ESP_LOGI(TAG, "RMT RCV --- got item (%d)", rx_size / 4);
      uint16_t rmt_addr;
      uint16_t rmt_cmd;
      int offset = 0;
      while (1) {
        // parse data value from ringbuffer.
        int res = nec_parse_items(item + offset, rx_size / 4 - offset, &rmt_addr, &rmt_cmd);
        if (res > 0) {
          offset += res + 1;
          ESP_LOGI(TAG, "RMT RCV --- addr: 0x%04x cmd: 0x%04x", rmt_addr, rmt_cmd);
          if (nec_rx_handler != NULL) {
            nec_rx_handler((uint8_t)(rmt_addr >> 8), (uint8_t)(rmt_addr & 0xFF),
                           (uint8_t)(rmt_cmd >> 8), (uint8_t)(rmt_cmd & 0xFF));
          }
        } else {
//          ESP_LOGI(TAG, "RMT RCV --- nec_parse_item returned %d", res);
          break;
        }
      }
      // after parsing the data, return spaces to ringbuffer.
      vRingbufferReturnItem(rb, (void *)item);
    }
  }
  vTaskDelete(NULL);
}

esp_err_t rmt_rx_enable() {
    rmt_rx_start(RMT_RX_CHANNEL, 0);
    return ESP_OK;
}

esp_err_t rmt_rx_disable() {
    rmt_rx_stop(RMT_RX_CHANNEL);
    return ESP_OK;
}

esp_err_t rmt_nec_tx_bytes(unsigned char *data, size_t data_len) {
  ESP_LOGI(TAG, "RMT SND --- data len %d", data_len);
  int channel = RMT_TX_CHANNEL;
  // each item represent a cycle of waveform.
  int item_num       = NEC_DATA_ITEM_NUM * (data_len / 4) * 8;
  size_t size        = (sizeof(rmt_item32_t) * item_num);
  rmt_item32_t *item = (rmt_item32_t *)calloc(sizeof(rmt_item32_t), item_num);
  int i, offset = 0, byte_index = 0;
  while (byte_index < data_len) {
    // To build a series of waveforms.
    i = nec_build_items(channel, item + offset, item_num - offset,
                        (data[byte_index] << 8 | data[byte_index + 1]),
                        (data[byte_index + 2] << 8 | data[byte_index + 3]));
    if (i < 0) {
      break;
    }
    offset += i;
    byte_index += 4;
  }
  // To send data according to the waveform items.
  rmt_write_items(channel, item, item_num, true);
  // Wait until sending is done.
  rmt_wait_tx_done(channel, portMAX_DELAY);
  // before we free the data, make sure sending is already done.
  free(item);
  return ESP_OK;
}

esp_err_t rmt_set_nec_rx_callback(void (*handler)(uint8_t, uint8_t, uint8_t, uint8_t)) {
  nec_rx_handler = handler;
  return ESP_OK;
}
static void nec_tx_task()
{
    vTaskDelay(10);
    nec_tx_init();
    esp_log_level_set(TAG, ESP_LOG_INFO);
    int channel = RMT_TX_CHANNEL;
    uint16_t cmd = 0x0;
    uint16_t addr = 0x11;
    int nec_tx_num = RMT_TX_DATA_NUM;
    for(;;) {
        ESP_LOGI(TAG, "RMT TX DATA");
        size_t size = (sizeof(rmt_item32_t) * NEC_DATA_ITEM_NUM * nec_tx_num);
        //each item represent a cycle of waveform.
        rmt_item32_t* item = (rmt_item32_t*) malloc(size);
        int item_num = NEC_DATA_ITEM_NUM * nec_tx_num;
        memset((void*) item, 0, size);
        int i, offset = 0;
        while(1) {
            //To build a series of waveforms.
            i = nec_build_items(channel, item + offset, item_num - offset, ((~addr) << 8) | addr, ((~cmd) << 8) |  cmd);
            if(i < 0) {
                break;
            }
            cmd++;
            addr++;
            offset += i;
        }
        //To send data according to the waveform items.
        rmt_write_items(channel, item, item_num, true);
        //Wait until sending is done.
        rmt_wait_tx_done(channel, portMAX_DELAY);
        //before we free the data, make sure sending is already done.
        free(item);
        vTaskDelay(2000 / portTICK_PERIOD_MS);
    }
    vTaskDelete(NULL);
}

esp_err_t driver_rmt_init(void) {
  nec_rx_init();
  nec_tx_init();
  xTaskCreate(nec_rx_task, "rmt_nec_rx_task", 2048, NULL, 10, NULL);
//  xTaskCreate(nec_tx_task, "rmt_nec_tx_task", 2048, NULL, 10, NULL);
  ESP_LOGD(TAG, "init done");
  return ESP_OK;
}

#else  // DRIVER_I2C_ENABLE
esp_err_t driver_rmt_init(void) {
  return ESP_OK;
}  // Dummy function, leave empty!
#endif
