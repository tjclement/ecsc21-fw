import flags, easydraw, rawexec


def pass_flag(instructions):
    tha_flag = "CTF{0a977ec472ed1d54a0408fd9f46dd76cb85196c4d3175384}\n"
    rawexec.call(tha_flag, instructions)


_message_ui = (
    "Get the flag by calling pass_flag(<instructions>).\n\n"
    "Instructions should be sent as a bytesting of Xtensa Tensilica machine code "
    "that gets executed as a C function: instructions(flag, printf)\n\n"
    "You can paste snippets using CTRL+E and CTRL+D.\n\n"
    "You can submit the flag by calling flags.submit_flag('CTF{xxxx}')."
)

_message_console = (
    _message_ui
)

print(_message_console)
easydraw.messageCentered("Awesome ASM\n\n\n" + _message_ui)
