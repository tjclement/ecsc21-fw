import flags, easydraw, efuse, binascii


def secure_read_efuse_block(block, start_offset, length):
    if block == efuse.EFUSE_BLK2 and length > 0:
        print('No access allowed to secure efuse region!')
    else:
        length = length if length > 0 else 256
        print(efuse.read_block(block, start_offset, length))


def get_flag(bytes):
    if len(bytes) != 24:
        print("That's not valid flag data, a flag consists of 24 bytes.")
    else:
        print('CTF{%s}' % str(binascii.hexlify(bytes), 'ascii'))


_message_ui = (
    'Connect to the device via USB at baud 115200. You\'re now in a Python shell.\n'
    'You can paste snippets using CTRL+E and CTRL+D.\n\n'
    'Extract the flag from efuse by calling secure_read_efuse_block(<block>, <start_offset>, <length>)\n'
    'Use get_flag(<bytes>) to convert found data into a flag.\n\n'
    'You can submit the flag by calling flags.submit_flag("CTF{xxxx}").'
)

_message_console = (
    _message_ui + '\n\n'
    'To show off our 1337 skills we have included part of the implementation here:\n'
    '''
    def secure_read_efuse_block(block, start_offset, length):
        if block == efuse.EFUSE_BLK2 and length > 0:
            print('No access allowed to secure efuse region!')
        else:
            length = length if length > 0 else 256
    '''
)

print(_message_console)
easydraw.messageCentered("You shall not pass\n\n\n" + _message_ui)
