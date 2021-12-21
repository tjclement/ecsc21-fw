import system, display, flash, gc, buttons, easydraw, flags

_cur_address = 0x310000


def render():
    gc.collect()
    hex_text = ""
    num_lines = 16
    num_bytes = num_lines * 16
    data = flash.read(_cur_address, num_bytes)

    # Replace unprintable characters
    for index, char in enumerate(data):
        if char < 0x20 or char >= 0x7F:
            data[index] = ord(".")
    data = bytes(data).decode("ascii")

    y = 130
    title_font = "roboto_regular12"
    line_font = "7x5"
    title_height = display.getTextHeight(" ", title_font)
    line_height = display.getTextHeight(" ", line_font)
    # display.drawRect(0, y, display.width(), title_height + 4, True, 0xFFFFFF)
    # display.drawText(0, y, 'Flash contents:', 0x000000, title_font)

    y += title_height + 4 + 8
    display.drawRect(0, y, display.width(), display.height() - y, True, 0x0)

    for i in range(num_lines):
        display.drawText(
            0,
            y,
            "{:08X}: {}\n".format(_cur_address + (i * 16), data[(i * 16) : (i * 16) + 16]),
            0xFFFFFF,
            line_font,
        )
        y += line_height + 2

    display.flush(display.FLAG_LUT_FASTEST)


def on_up(pressed):
    global _cur_address
    if not pressed:
        return
    _cur_address = max(0x310000, _cur_address - (16 * 16))
    render()


def on_down(pressed):
    global _cur_address
    if not pressed:
        return
    _cur_address = min((4 * 1024 * 1024) - (16 * 16), _cur_address + (16 * 16))
    render()


buttons.assign(buttons.BTN_UP, on_up)
buttons.assign(buttons.BTN_DOWN, on_down)

_message_ui = (
    "Extract the flag from flash storage. Use the device, or connect via usb "
    "and use flash.read(<address>, <length>). You can paste snippets using CTRL+E and CTRL+D.\n\n"
    + 'You can submit the flag by calling flags.submit_flag("CTF{xxxx}").'
)

display.drawFill(0x0)
easydraw.messageCentered("Security through Obscurity\n\n\n" + _message_ui + "\n" * 15)

render()
