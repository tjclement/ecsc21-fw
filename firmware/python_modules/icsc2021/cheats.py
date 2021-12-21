import flags, valuestore, listbox, display, buttons

challnames = []
items = []
points = []


def run():
    _challs = {
        "1a": {"name": "Script Kiddie", "points": 100},
        "1b": {"name": "King of Regex", "points": 100},
        "1c": {"name": "Security through Obscurity", "points": 100},
        "1d": {"name": "Timing is Key", "points": 200},
        "1e": {"name": "Sailing in Side Channels", "points": 200},
        "1f": {"name": "One Time Pwn", "points": 200},
        "2a": {"name": "Zagan's IP", "points": 100},
        "2b": {"name": "Zagan's Bitcoin Wallet", "points": 200},
        "2c": {"name": "Zagan's Address", "points": 500},
    }

    found_flags = valuestore.load(keyname="flags")
    for key in _challs.keys():
        if key not in found_flags:
            challnames.append(key)
            items.append(_challs[key]["name"])
            points.append(_challs[key]["points"])

    list = listbox.List(0, 0, 240, 320)
    for item in items:
        list.add_item(item)

    def _on_up(pressed):
        if not pressed:
            return
        list.moveUp()
        display.flush()

    def _on_down(pressed):
        if not pressed:
            return
        list.moveDown()
        display.flush()

    def _on_right(pressed):
        if not pressed:
            return
        index = list.selected_index()
        chall = challnames[index]
        points_no = points[index]
        flags.submit_flag(flags.create_flag(chall, points_no))
        list.remove_item(index)
        del challnames[index], points[index], items[index]
        list.draw()
        display.flush()

    buttons.assign(buttons.BTN_UP, _on_up)
    buttons.assign(buttons.BTN_DOWN, _on_down)
    buttons.assign(buttons.BTN_RIGHT, _on_right)

    list.draw()
    display.flush()


run()
