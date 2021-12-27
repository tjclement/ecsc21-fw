import flags, easydraw, rawexec


def pass_flag(instructions):
    """
    *** SOLUTION ***

    A possible solution to this challenge can be to create a c file called solution.c
    with the following contents:

        typedef int (*printf_ptr) (const char *, ...);

        void func(const char *str, printf_ptr call_printf) {
            call_printf(str);
        }

    And then compile this file using the Xtensa ESP32 Toolchain:

    $ xtensa-esp32-elf-gcc -c solution.c

    Then dissamble the created object file by running:

    $ xtensa-esp32-elf-objdump -d solution.o

    Which will give you the required Xtensa Tensilica machine code:

       0:	006136      entry	a1, 48
       3:	017d      	mov.n	a7, a1
       5:	0729      	s32i.n	a2, a7, 0
       7:	1739      	s32i.n	a3, a7, 4
       9:	1728      	l32i.n	a2, a7, 4
       b:	07a8      	l32i.n	a10, a7, 0
       d:	0002e0      callx8	a2
      10:	f03d      	nop.n
      12:	f01d      	retw.n

    Which needs to be properly put in a python bytestring using the right alignment and then
    used in the call to `pass_flag()`:

    >>> pass_flag(b"\x36\x61\x00\x7D\x01\x29\x07\x39\x17\x28\x17\xa8\x07\xe0\x02\x00\x3d\xf0\x1d\xf0")
    assembly_len: 20, assembly location: 0x4008c8fc, first dword: 7D006136
    0x4008c8fc: esp_flash_user_start at modesp.c:?

    CTF{0a977ec472ed1d54a0408fd9f46dd76cb85196c4d3175384}
    """
    tha_flag = "CTF{0a977ec472ed1d54a0408fd9f46dd76cb85196c4d3175384}\n"
    rawexec.call(tha_flag, instructions)


_message_ui = (
    "Get the flag by calling pass_flag(<instructions>).\n\n"
    "Instructions should be sent as a bytesting of Xtensa Tensilica machine code "
    "that gets executed as a C function: instructions(flag, printf)\n\n"
    "You can paste snippets using CTRL+E and CTRL+D.\n\n"
    "You can submit the flag by calling flags.submit_flag('CTF{xxxx}')."
)

_message_console = _message_ui

print(_message_console)
easydraw.messageCentered("Awesome ASM\n\n\n" + _message_ui)
