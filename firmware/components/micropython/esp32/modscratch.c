#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/runtime.h"

#include "esp_err.h"
#include "esp_partition.h"
#include "esp_spi_flash.h"

#include <driver_i2c.h>

#define FLASH_PAGE_SIZE 4096
static esp_partition_t *custom1 = NULL;

STATIC mp_obj_t scratch_read_(mp_obj_t _offset, mp_obj_t _length) {
    int offset = mp_obj_get_int(_offset);
    int length  = mp_obj_get_int(_length);
    uint32_t aligned_offset = offset & 0xFFFFF000; // Aligned to 4k page boundary

    if (offset < 0 || offset > 4*FLASH_PAGE_SIZE) {
        mp_raise_msg(&mp_type_ValueError, "offset out of range");
        return mp_const_none;
    }

    if (length < 1 || length > 4*FLASH_PAGE_SIZE) {
        mp_raise_msg(&mp_type_ValueError, "length out of range");
        return mp_const_none;
    }

    if (custom1 == NULL) {
        custom1 = esp_partition_find_first(0x40, 0x0, "custom1");
        if (custom1 == NULL) {
            mp_raise_msg(&mp_type_OSError, "scratch partition is missing");
            return mp_const_none;
        }
    }

    vstr_t vstr;
    vstr_init_len(&vstr, length);

    if (esp_partition_read(custom1, offset, (void*)vstr.buf, length) != ESP_OK) {
        mp_raise_msg(&mp_type_OSError, "failed to read from scratch partition");
        return mp_const_none;
    }

    return mp_obj_new_str_from_vstr(&mp_type_bytes, &vstr);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(scratch_read_obj, scratch_read_);

void introduce_cell_fatigue_effect(char* data, int data_length) {
    int random = rand();

    // Every write, we introduce a single bit flip
    char failure = 1 << (random % 8);
    int offset = random % data_length;

    // Set failure bit to 1. It might already be, in which case nothing happens.
    data[offset] |= failure;
}

STATIC mp_obj_t scratch_write_(mp_obj_t _offset, mp_obj_t _data) {
    int offset = mp_obj_get_int(_offset);
    mp_uint_t data_len;
    uint8_t *data = (uint8_t *) mp_obj_str_get_data(_data, &data_len);
    uint32_t aligned_offset = offset & 0xFFFFF000; // Aligned to 4k page boundary
    uint32_t offset_in_page = offset & 0xFFF;

    if (offset < 0 || offset > 4*FLASH_PAGE_SIZE) {
        mp_raise_msg(&mp_type_ValueError, "offset out of range");
        return mp_const_none;
    }

    if (data_len < 1 || data_len > FLASH_PAGE_SIZE) {
        mp_raise_msg(&mp_type_ValueError, "data length out of range");
        return mp_const_none;
    }

    if ((offset_in_page + data_len) > FLASH_PAGE_SIZE) {
        mp_raise_msg(&mp_type_ValueError, "can't write across 4k page borders");
        return mp_const_none;
    }

    if ((offset + data_len) >= 0x0FFC && (offset + data_len) <= 0x1000) {
        mp_raise_msg(&mp_type_ValueError, "refusing to write values into access permission bits at 0x0FFC-0x0FFF");
        return mp_const_none;
    }

    // First we read the entire 4k page into memory
    char* buffer = malloc(FLASH_PAGE_SIZE);

    if (custom1 == NULL) {
        custom1 = esp_partition_find_first(0x40, 0x0, "custom1");
        if (custom1 == NULL) {
            mp_raise_msg(&mp_type_OSError, "scratch partition is missing");
            return mp_const_none;
        }
    }

    if (esp_partition_read(custom1, aligned_offset, (void*)buffer, FLASH_PAGE_SIZE) != ESP_OK) {
        mp_raise_msg(&mp_type_OSError, "failed to read from scratch partition");
        free(buffer);
        return mp_const_none;
    }

    // Then we modify the local buffer with the given data
    for (int i=0; i < data_len; i++) {
        buffer[offset + i] = data[i];
    }

    // Then we fake accelerated flash cell fatigue to introduce 0>1 bitflips
    introduce_cell_fatigue_effect(buffer, FLASH_PAGE_SIZE);

    // Then we erase the 4k page on flash
    if (esp_partition_erase_range(custom1, aligned_offset, FLASH_PAGE_SIZE) != ESP_OK) {
        mp_raise_msg(&mp_type_OSError, "failed to erase scratch page");
        free(buffer);
        return mp_const_none;
    }

    // And finally we write the modified data back to flash
    if (esp_partition_write(custom1, aligned_offset, (void*)buffer, FLASH_PAGE_SIZE) != ESP_OK) {
        mp_raise_msg(&mp_type_OSError, "failed to write to scratch partition");
        free(buffer);
        return mp_const_none;
    }

    free(buffer);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(scratch_write_obj, scratch_write_);

STATIC const mp_rom_map_elem_t scratch_module_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&scratch_read_obj)},
    {MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&scratch_write_obj)},
};

STATIC MP_DEFINE_CONST_DICT(scratch_module_globals, scratch_module_globals_table);

const mp_obj_module_t scratch_module = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&scratch_module_globals,
};
