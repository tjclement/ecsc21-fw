#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/runtime.h"

typedef int (*printf_ptr) (const char *str, ...);
typedef void (*assembly_ptr) (const char *str, printf_ptr);
typedef void (*simple_ptr) ();

static IRAM_ATTR uint8_t assembly[4096] = {0};


STATIC mp_obj_t rawexec_call_(mp_obj_t _text, mp_obj_t _assembly) {
    mp_uint_t text_len;
    const char *text = (char *) mp_obj_str_get_data(_text, &text_len);

    bool is_bytes = MP_OBJ_IS_TYPE(_assembly, &mp_type_bytes);
    if (!is_bytes) {
        mp_raise_msg(&mp_type_AttributeError, "Assembly should be a bytestring");
    }

    // Workaround for issue where IRAM_ATTR uint8_t array is not saved 4-byte
    // aligned in memory.
    uint8_t* aligned_assembly = assembly;
    while(aligned_assembly % 4 !== 0) {
        aligned_assembly++;
    }

    mp_uint_t assembly_len;
    uint8_t* assembly_pointer = (uint8_t *) mp_obj_str_get_data(_assembly, &assembly_len);
    printf(
        "assembly_len: %d, assembly location: %p, first dword: %04X\n",
         assembly_len, aligned_assembly, *((uint32_t*)assembly_pointer)
    );
    fflush(stdout);

    memcpy(aligned_assembly, assembly_pointer, assembly_len);

    simple_ptr call_assembly = aligned_assembly;
    call_assembly();

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(rawexec_call_obj, rawexec_call_);

STATIC const mp_rom_map_elem_t rawexec_module_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR_call), MP_ROM_PTR(&rawexec_call_obj)},
};

STATIC MP_DEFINE_CONST_DICT(rawexec_module_globals, rawexec_module_globals_table);

const mp_obj_module_t rawexec_module = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&rawexec_module_globals,
};
