import ure, easydraw, time, flags
from term import prompt, clear

_regex_literal = r'([^\W][\b]\\\\\w\w\w[^\d|\w])I\sr\x13\x37|\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w(133\x37)+?'
_regex = '([^\W][\b]\\\\\w\w\w[^\d|\w])I\sr\x13\x37|\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w(133\x37)+?'
_message_ui = 'Connect to your device via USB, and open a serial terminal. Provide a passphrase that matches the regular expression shown in your terminal.\n\n' + \
           'You can submit the flag by calling flags.submit_flag("CTF{xxxx}").'
_message_console = 'Provide a passphrase that matches to the following regular expression:\n\n' + _regex_literal

easydraw.messageCentered('King of Regex\n\n\n' + _message_ui)

while True:
    clear()
    phrase = prompt(_message_console + '\n\nYour phrase', 0, 0, colors=False)
    result = ure.match(_regex, phrase)
    if result is None:
        print('\n\nIncorrect!')
        time.sleep(1)
        continue
    else:
        print('\n\nCorrect! Here\'s your flag: CTF{61ff6d23c29f5bcf873f093b29c6a0c306cd889aefb63e1f}')
        break