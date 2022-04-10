import listbox, valuestore, display, virtualtimers, machine


def run():
    import flags  # Import needs to be delayed to work around LoadStoreError crash

    _challnames = {
        "1a": "You shall not pass",
        "1b": "Insane in the Membrain",
        "1c": "Got root?",
        "1d": "RTFM",
        "1e": "Wear and tear",
        "1f": "Awesome ASM",
        "1g": "Eccentric exfiltration",
    }

    found_flags = flags.get_found_flags()

    items = []
    total_points = 0

    for challenge, points in found_flags.items():
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
