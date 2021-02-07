//
// Created by Tom on 07/02/2021.
//


//#include <sdkconfig.h>
#include "../../../build/include/sdkconfig.h"

#ifdef CONFIG_DRIVER_RMT_ENABLE

#include <string.h>

#include "esp_log.h"

#include "py/obj.h"
#include "py/objstr.h"
#include "py/mphal.h"
#include "py/mperrno.h"
#include "py/runtime.h"
#include "lib/utils/pyexec.h"

#include <driver_rmt.h>

#define TAG "esp32/touchbuttons"

static mp_obj_t nec_rx_callback = mp_const_none;

static void _nec_rx_handler(uint8_t addr1, uint8_t addr2, uint8_t cmd1, uint8_t cmd2) {
    if (nec_rx_callback != mp_const_none) {
        // uPy scheduler tends to get full for unknown reasons, so to not lose any interrupts,
        // we try until the schedule succeeds.
        unsigned char orig_data[] = {
            addr1,
            addr2,
            cmd1,
            cmd2,
        };
        mp_obj_t data = mp_obj_new_bytes(orig_data, 4);
        bool succeeded = mp_sched_schedule(nec_rx_callback, data, NULL);
        while (!succeeded) {
            ESP_LOGW(TAG, "Failed to call IR RMT callback, retrying");
            succeeded = mp_sched_schedule(nec_rx_callback, data, NULL);
        }
    }
}

static mp_obj_t enable_rx(mp_obj_t handler) {
  esp_err_t result = rmt_rx_enable();
  return result == ESP_OK ? mp_const_true : mp_const_false;
}
static MP_DEFINE_CONST_FUN_OBJ_0(enable_rx_obj, enable_rx);

static mp_obj_t disable_rx(mp_obj_t handler) {
  esp_err_t result = rmt_rx_disable();
  return result == ESP_OK ? mp_const_true : mp_const_false;
}
static MP_DEFINE_CONST_FUN_OBJ_0(disable_rx_obj, disable_rx);

static mp_obj_t nec_rx_handler(mp_obj_t handler) {
  nec_rx_callback = handler;
  rmt_set_nec_rx_callback(&_nec_rx_handler);
  return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(nec_rx_handler_obj, nec_rx_handler);

static mp_obj_t nec_tx_bytes(mp_obj_t data) {
  mp_uint_t data_len;
  unsigned char* cast_data = mp_obj_str_get_data(data, &data_len);
  esp_err_t result = rmt_nec_tx_bytes(cast_data, data_len);
  return result == ESP_OK ? mp_const_true : mp_const_false;
}
static MP_DEFINE_CONST_FUN_OBJ_1(nec_tx_bytes_obj, nec_tx_bytes);


static const mp_rom_map_elem_t rmt_module_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_rmt)},
    {MP_ROM_QSTR(MP_QSTR_enable_rx), MP_ROM_PTR(&enable_rx_obj)},
    {MP_ROM_QSTR(MP_QSTR_disable_rx), MP_ROM_PTR(&disable_rx_obj)},
    {MP_ROM_QSTR(MP_QSTR_nec_rx_handler), MP_ROM_PTR(&nec_rx_handler_obj)},
    {MP_ROM_QSTR(MP_QSTR_nec_tx_bytes), MP_ROM_PTR(&nec_tx_bytes_obj)},
};

static MP_DEFINE_CONST_DICT(rmt_module_globals, rmt_module_globals_table);

const mp_obj_module_t rmt_module = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&rmt_module_globals,
};

#endif
