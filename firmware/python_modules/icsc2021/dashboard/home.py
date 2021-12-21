import buttons, easydraw, display, machine, system, virtualtimers
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
    header="WARNING: this device is being wiped remotely.",
    logo="/private/system/logo_small.png",
)

_menu_items = {
    _menu: [
        ("Newbie CTF Entrance Exam", lambda: ""),
        ("View found flags", lambda: system.start("showflags")),
        ("(debug) Cheats", lambda: system.start("cheats")),
        ("(debug) Shell", lambda: system.start("shell")),
        ("(debug) Update firmware", lambda: system.start("force_update")),
        ("(debug) Factory reset", lambda: system.start("reset")),
        ("(debug) IR Test", lambda: system.start("emergency")),
    ],
}


_menu_stack = []


def _build_menu():
    global _menu_stack, _menu_items

    for menu, items in _menu_items.items():
        for item in items:
            name, value = item
            menu.add_item(name)

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
    name, value = _menu_items[current_menu][selected_index]
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


def update_countdown():
    _menu.countdown_time -= 1

    # Protect nvs by persisting the timer only once each 10 seconds
    if _menu.countdown_time % 10 == 0:
        machine.nvs_setint("system", "countdown_time", _menu.countdown_time)

    _menu_stack[-1].draw()
    display.flush()

    return 1000  # Run again in 1 sec


virtualtimers.begin(1000)
virtualtimers.new(0, update_countdown)
