# print("Welcome to the shell of your ESP32 device!")
# print("Type 'import menu' to enter the menu.")

import buttons, display, machine, system
from listbox import List

_challenge1a = 'challenges.1a'
_challenge1b = 'challenges.1b'
_challenge1c = 'challenges.1c'
_challenge1d = 'challenges.1d'
_challenge1e = 'challenges.1e'
_challenge1f = 'challenges.1f'


# Logo LED
_pin2=machine.PWM(15, freq=40000, duty=50)
display.orientation(270)


_top_menu = List(0, 0, display.width(), display.height())
_challenge_menu = List(0, 0, display.width(), display.height())

_menu_items = {
    _top_menu: [
        ('Newbie CTF Entrance Exam', _challenge_menu),
        ('View found flags', lambda: system.start('showflags')),
        ('(debug) Cheats', lambda: system.start('cheats')),
        ('(debug) Shell', lambda: system.start('shell')),
        ('(debug) Update firmware', lambda: system.start('force_update')),
        ('(debug) Factory reset', lambda: system.start('reset')),
    ],
    _challenge_menu: [
        ('Script Kiddie', lambda: system.start(_challenge1a)),
        ('King of Regex', lambda: system.start(_challenge1b)),
        ('Security through Obscurity', lambda: system.start(_challenge1c)),
        ('Timing is Key', lambda: system.start(_challenge1d)),
        ('Sailing in Side Channels', lambda: system.start(_challenge1e)),
        ('One Time Pwn', lambda: system.start(_challenge1f)),
    ],
}

for menu, items in _menu_items.items():
    for item in items:
        name, value = item
        menu.add_item(name)

_menu_stack = [_top_menu]

def _on_up(pressed):
    if not pressed:
        return
    _menu_stack[-1].moveUp()
    display.flush()

def _on_down(pressed):
    if not pressed:
        return
    _menu_stack[-1].moveDown()
    display.flush()

def _on_left(pressed):
    global _menu_stack
    if not pressed:
        return
    if len(_menu_stack) > 1:
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

buttons.pushMapping({
    buttons.BTN_UP: _on_up,
    buttons.BTN_DOWN: _on_down,
    buttons.BTN_LEFT: _on_left,
    buttons.BTN_RIGHT: _on_right})

_menu_stack[-1].draw()
display.flush()