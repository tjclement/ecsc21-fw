import buttons, easydraw, display, machine, system, virtualtimers, flags, time
from listbox import List

# Logo LED
_pin2 = machine.PWM(15, freq=40000, duty=50)
display.orientation(270)

_showing_details = False

countdown_time = machine.nvs_getint("system", "countdown_time") or 28800  # By default start with 8 hours countdown

_menu = List(
    0,
    0,
    display.width(),
    display.height(),
    countdown_time=countdown_time,
    header="WARNING: this will be wiped remotely if protection mechanisms are not disabled in:",
    logo="/private/system/logo_small.png",
)

found_flags = flags.get_found_flags()

_menu_items = {
    _menu: [
        # ("View found flags", None, None, lambda: system.start("showflags")),
        ("You shall not pass", "1a" in found_flags, 100, lambda: system.start("challenges.1a")),
        ("Insane in the membrain", "1b" in found_flags, 200, lambda: system.start("challenges.1b")),
        ("Got root?", "1c" in found_flags, 200, lambda: system.start("challenges.1c")),
        ("RTFM", "1d" in found_flags, 300, lambda: system.start("challenges.1d")),
        ("Wear and tear", "1e" in found_flags, 300, lambda: system.start("challenges.1e")),
        ("Awesome ASM", "1f" in found_flags, 300, lambda: system.start("challenges.1f")),
        ("Eccentric exfiltration", "1g" in found_flags, 700, lambda: system.start("challenges.1g")),
    ],
}


_menu_stack = []


def _build_menu():
    global _menu_stack, _menu_items

    for menu, items in _menu_items.items():
        for item in items:
            name, is_unlocked, points, _ = item
            menu.add_item(name, is_unlocked, points)

    _menu_stack = [_menu]


def _on_up(pressed):
    global _showing_details
    if not pressed:
        return
    elif _showing_details:
        _showing_details = False
    _menu_stack[-1].moveUp()
    display.flush()


def _on_down(pressed):
    global _showing_details
    if not pressed:
        return
    elif _showing_details:
        _showing_details = False
    _menu_stack[-1].moveDown()
    display.flush()


def _on_left(pressed):
    global _menu_stack, _showing_details
    if not pressed:
        return
    elif _showing_details:
        # If in a detail view (email, job, etc), exit it by redrawing the menu on top of it
        _showing_details = False
    elif len(_menu_stack) > 1:
        _menu_stack.pop()
    _menu_stack[-1].draw()
    display.flush()


def _on_right(pressed):
    global _menu_stack
    if not pressed:
        return
    current_menu = _menu_stack[-1]
    selected_index = current_menu.selected_index()
    name, _, _, value = _menu_items[current_menu][selected_index]
    if callable(value):
        value()
    elif isinstance(value, List):
        _menu_stack.append(value)
        current_menu = _menu_stack[-1]
        current_menu.draw()

    display.flush()


buttons.pushMapping(
    {
        buttons.BTN_UP: _on_up,
        buttons.BTN_DOWN: _on_down,
        buttons.BTN_LEFT: _on_left,
        buttons.BTN_RIGHT: _on_right,
    }
)

_build_menu()
_menu_stack[-1].draw()
display.flush()


def menu_countdown_tick():
    # start = time.time()
    _menu.countdown_time -= 1
    _menu_stack[-1].draw_timer(1, 137)
    display.flush()
    # end = time.time()
    # print("took:", end-start)

    return 1000  # Run again in 1 sec


# virtualtimers.begin is already called in boot.py
virtualtimers.new(0, menu_countdown_tick)
