
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/runtime.h"

#include "backported_efuse.h"

STATIC mp_obj_t efuse_read_block_(mp_obj_t _block, mp_obj_t _offset, mp_obj_t _length) {
    int block = mp_obj_get_int(_block);
    int offset = mp_obj_get_int(_offset);
    int length  = mp_obj_get_int(_length);

    if (block < 0 || block > 3) {
        mp_raise_msg(&mp_type_ValueError, "Invalid efuse block");
    }

    if (offset < 0 || offset > 255) {
        mp_raise_msg(&mp_type_ValueError, "Invalid bit offset");
    }

    if (length < 0 || length > 256) {
        mp_raise_msg(&mp_type_ValueError, "Invalid amount of bits to read");
    }

    if (offset + length > 256) {
        mp_raise_msg(&mp_type_ValueError, "Cannot read outside of block");
    }

    if (length % 8 != 0) {
        mp_raise_msg(&mp_type_ValueError, "Number of bits to read should be multiple of 8");
    }

    vstr_t vstr;
    vstr_init_len(&vstr, length/8);

    if (esp_efuse_read_block(block, (uint8_t *) vstr.buf, offset, length) != ESP_OK) {
        mp_raise_OSError(MP_EIO);
    }

    return mp_obj_new_str_from_vstr(&mp_type_bytes, &vstr);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_3(efuse_read_block_obj, efuse_read_block_);

STATIC const mp_rom_map_elem_t efuse_module_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR_read_block), MP_ROM_PTR(&efuse_read_block_obj)},
    {MP_ROM_QSTR(MP_QSTR_EFUSE_BLK0), MP_ROM_INT(EFUSE_BLK0) },
    {MP_ROM_QSTR(MP_QSTR_EFUSE_BLK1), MP_ROM_INT(EFUSE_BLK1) },
    {MP_ROM_QSTR(MP_QSTR_EFUSE_BLK2), MP_ROM_INT(EFUSE_BLK2) },
    {MP_ROM_QSTR(MP_QSTR_EFUSE_BLK3), MP_ROM_INT(EFUSE_BLK3) },
};

STATIC MP_DEFINE_CONST_DICT(efuse_module_globals, efuse_module_globals_table);

const mp_obj_module_t efuse_module = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&efuse_module_globals,
};