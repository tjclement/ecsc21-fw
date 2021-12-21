import listbox, valuestore, display, virtualtimers, machine


def run():
    import flags  # Import needs to be delayed to work around LoadStoreError crash

    _challnames = {
        "1a": "Script Kiddie",
        "1b": "King of Regex",
        "1c": "Security through Obscurity",
        "1d": "Timing is Key",
        "1e": "Sailing in Side Channels",
        "1f": "One Time Pwn",
        "2a": "Zagan's IP",
        "2b": "Zagan's Bitcoin Wallet",
        "2c": "Zagan's Location",
    }

    found_flags = valuestore.load(keyname="flags")
    items = []
    total_points = 0

    for key in found_flags.keys():
        # print('Doing', key)
        flag = found_flags[key]["flag"]
        # print('flag', flag)
        result = flags.parse_flag(flag)
        # print('Found', result)
        if result is not None:
            challenge, points = result
            total_points += points
            items.append("%s (%d points)" % (_challnames[challenge], points))

    if len(items) == 0:
        items = ["You have not found any flags so far."]

    if total_points == 1700:
        items.append(" ")
        items.append("Well done, you've captured all flags!")

    list = listbox.List(0, 0, 240, 320, header="Current points: %d" % total_points)
    for item in items:
        list.add_item(item)

    display.flush()
    print("Flags found so far:", found_flags)

    return -1


run()
# virtualtimers.begin(500)
# virtualtimers.new(500, run)
