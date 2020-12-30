# print("Welcome to the shell of your ESP32 device!")
# print("Type 'import menu' to enter the menu.")

import buttons, easydraw, display, machine, system
from listbox import List

# Logo LED
_pin2=machine.PWM(15, freq=40000, duty=50)
display.orientation(270)

_name = machine.nvs_getint('system', 'nickname') or 'UnnamedHax0r'
_showing_details = False

_top_menu = List(0, 0, display.width(), display.height(),
                 header='Greetings, %s.' % _name, logo='/private/system/logo_small.png')
_challenge_menu = List(0, 0, display.width(), display.height())
_jobs_menu = List(0, 0, display.width(), display.height())
_messages_menu = List(0, 0, display.width(), display.height())
_intelligence_menu = List(0, 0, display.width(), display.height(), header='Submit info to Europol')

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
        ('Script Kiddie', lambda: system.start('challenges.1a')),
        ('King of Regex', lambda: system.start('challenges.1b')),
        ('Security through Obscurity', lambda: system.start('challenges.1c')),
        ('Timing is Key', lambda: system.start('challenges.1d')),
        ('Sailing in Side Channels', lambda: system.start('challenges.1e')),
        ('One Time Pwn', lambda: system.start('challenges.1f')),
    ],
    _jobs_menu: [],
    _messages_menu: [],
    _intelligence_menu: [
        ('Home IP (100 points)', lambda: system.start('submit.ip')),
        ('Bitcoin wallet address (200 points)', lambda: system.start('submit.wallet')),
        ('Home Address (500 points)', lambda: system.start('submit.address')),
    ]
}

if machine.nvs_getint('system', 'jobs_unlocked'):
    _menu_items[_top_menu].insert(2, ('Job board', _jobs_menu))
    _menu_items[_top_menu].insert(3, ('Message board', _messages_menu))
    _menu_items[_top_menu].insert(4, ('Emergency Contact', lambda: system.start('emergency')))
else:
    _top_menu.header += ' Complete 700 points from the entrance exam to unlock the job board.'

if machine.nvs_getint('system', 'message_seen'):
    _menu_items[_top_menu].insert(5, ('Europol Submissions', _intelligence_menu))

_menu_stack = []

def _build_menu():
    global _menu_stack, _menu_items

    jobs = [
        {
            'preview': 'Free Software Foundation: Windows 10 source code',
            'body': 'By: Zagan\nClient: Free Software Foundation\n\nAssignment:\n\n' + \
                    'Rumours allege that Windows might secretly use GPL-licensed content in their code base. ' + \
                    'This is of course absolutely disgusting for proprietary software, if true. ' + \
                    'Obtain a full copy so our client can investigate these claims.\n\n' + \
                    'Note: FSF is really cool. I donated some BTC on July 12th 2020 to support them, and so should you.'
        }
    ]
    # 5.62.42.125 5.62.40.117 5.62.42.107 vpn.hidemyass.com
    messages = [
        {
            'preview': '(now) Europol: New option on homescreen',
            'from': 'Zagan',
            'to': 'You',
            'body': 'By: Europol\n\nMessage:\n\n' + \
                    'Good work unlocking the device! We\'ve installed a new item onto your homescreen.' + \
                    'You can use this to send your findings on Zagan to us. Reboot your device to activate it.',
            'source': '144.76.240.11 (autoresolved: europol.europa.eu)'
        },
        {
            'preview': '(1d) Zagan: Be suspicious of new recruits',
            'from': 'Zagan',
            'to': 'Sixt Circle',
            'body': 'By: Zagan\n\nMessage:\n\n' + \
                    'It appears that some of our handhelds have gone missing. This is serious. ' + \
                    'We will be more vigilant to new recruits now, as we can\'t be sure they are who they say. ' + \
                    'The risk of moles is now real, so stay on your toes.',
            'source': '5.62.42.125 (autoresolved: vpn.hidemyass.com)'
        },
        {
            'preview': '(2d) Zagan: New credentials leaked',
            'from': 'Zagan',
            'to': 'Sixt Circle',
            'body': 'By: Zagan\n\nMessage:\n\n' + \
                    'Check out the huge credential database that just leaked from the IRS breach, it\'s amazing. ' + \
                    'Hundreds of millions of fresh logins, ready for some sweet credential stuffing. Enjoy.',
            'source': '109.235.128.209 (autoresolved: dinamyc-pool-209.direct-telecom.es)'
        }
    ]

    for job in jobs:
        _menu_items[_jobs_menu].append((job['preview'], lambda job=job: draw_job(job)))

    for message in messages:
        _menu_items[_messages_menu].append((message['preview'], lambda message=message: draw_message(message)))

    for menu, items in _menu_items.items():
        for item in items:
            name, value = item
            menu.add_item(name)

    _menu_stack = [_top_menu]


def draw_job(job):
    global _showing_details
    _showing_details = True
    print(job['body'])
    display.drawFill(0x0)
    easydraw.text(0, 0, job['body'])

def draw_message(message):
    global _showing_details
    _showing_details = True
    print('Received: from [136.167.40.119] (HELO dc.edu)\n' + \
    'by fe3.dc.edu (CommuniGate Pro SMTP 4.1.8)\n' + \
    'From: %s\n' % message['from'] + \
    '             User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.0.1) Gecko/20020823 Netscape/7.0' + \
    'X-Accept-Language: en-us, en\n' + \
    'X-Originating-IP: [%s]\n' % message['source'] + \
    'MIME-Version: 1.0\n' + \
    'To: %s\n' % message['to'] + \
    'Content-Type: text/plain; charset=us-ascii; format=flowed\n' + \
    'Content-Transfer-Encoding: 7bit\n')
    print(message['body'])
    display.drawFill(0x0)
    easydraw.text(0, 0, message['body'])

    if 'Europol' in message['preview'] and not machine.nvs_getint('system', 'message_seen'):
        machine.nvs_setint('system', 'message_seen', 1)

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

buttons.pushMapping({
    buttons.BTN_UP: _on_up,
    buttons.BTN_DOWN: _on_down,
    buttons.BTN_LEFT: _on_left,
    buttons.BTN_RIGHT: _on_right})

_build_menu()
_menu_stack[-1].draw()
display.flush()

import time
from ir import NecIR
infra = NecIR(badge='ecsc2021', freq=40000)
infra.command = lambda addr, cmd: print('Got', addr, cmd)
infra.rx_enable()
while True:
    infra.tx(0x13, 0x37)
    print(infra.buffer)
    time.sleep(2)
    # time.sleep(0.5)
