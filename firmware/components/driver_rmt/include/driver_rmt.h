#ifndef DRIVER_I2C_H
#define DRIVER_I2C_H

#include <stdint.h>
#include <esp_err.h>

__BEGIN_DECLS

esp_err_t driver_rmt_init();
esp_err_t rmt_rx_enable();
esp_err_t rmt_rx_disable();
esp_err_t rmt_set_nec_rx_callback(void (*handler)(uint8_t, uint8_t, uint8_t, uint8_t));
esp_err_t rmt_nec_tx_bytes(unsigned char *data, size_t data_len);

__END_DECLS

#endif // DRIVER_I2C_H
