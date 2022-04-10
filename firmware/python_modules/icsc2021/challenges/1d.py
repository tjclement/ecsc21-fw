import machine, display, easydraw, flags, scratch

def read_rtc_memory(address, length):
    if length % 4 != 0:
        raise ValueError("length must be a multiple of 4 bytes")

    if not (0x3FF80000 <= address <= 0x3FF81FFF) and not (0x400C0000 <= address <= 0x400C1FFF):
        raise ValueError("can only read from RTC_FAST memory, not normal RAM")

    if (0x3FF80000 <= address <= (0x3FF80000+53)):
        raise ValueError("refusing to read from security-sensitive address range 0x3FF80000-0x3FF80035")

    if address >= 0x40080000:
        print("Reading from IRAM")

    return b''.join([int.to_bytes(machine.mem32[address+i], 4, "little") for i in range(0, length, 4)])

_message_ui = 'The flag resides in RTC_FAST memory at address 0x3FF80000.\n\n' + \
              'Use read_rtc_memory(address, length) to access raw data in RTC RAM and find the flag.\n\n' + \
              'You can paste snippets using CTRL+E and CTRL+D.\n\n' + \
              'You can submit the flag by calling flags.submit_flag("CTF{xxxx}").'

_message_console = _message_ui

display.drawFill(0x0)
easydraw.messageCentered('RTFM\n\n\n' + _message_ui + '\n' * 8)

print(_message_console)
