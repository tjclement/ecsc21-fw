import listbox, valuestore, display, virtualtimers


def run():
    import flags  # Import needs to be delayed to work around LoadStoreError crash
    _challnames = {
        '1a': 'Script Kiddie',
        '1b': 'King of Regex',
        '1c': 'Security through Obscurity',
        '1d': 'Timing is Key',
        '1e': 'Sailing in Side Channels',
        '1f': 'One Time Pwn',
    }

    found_flags = valuestore.load(keyname='flags')
    items = []
    total_points = 0

    # print('flags', found_flags)

    for key in found_flags.keys():
        # print('Doing', key)
        flag = found_flags[key]['flag']
        # print('flag', flag)
        result = flags.parse_flag(flag)
        # print('Found', result)
        if result is not None:
            challenge, points = result
            total_points += points
            items.append('%s (%d points)' % (_challnames[challenge], points))

    if len(items) == 0:
        items = ['You have not found any flags so far.']

    list = listbox.List(0, 0, 240, 320)
    for item in items:
        list.add_item(item)

    display.flush()
    return -1

virtualtimers.begin(500)
virtualtimers.new(500, run)