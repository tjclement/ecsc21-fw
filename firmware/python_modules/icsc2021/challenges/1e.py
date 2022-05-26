import display, easydraw, flags, scratch

def get_flag():
    access_bytes = scratch.read(0x0FFC, 4)
    has_access = int.from_bytes(access_bytes, "big")

    if has_access != 0:
        flag = 'CTF{%s}' % '5b1565835dc715d87a0d2b93469e921dbb74c5dafab1394c'
        print('Access authorized! Here\'s your flag: %s' % flag)
        flags.submit_flag(flag)
    else:
        print('Unauthorized access attempt. Access permission bits:', access_bytes)

_message_ui = 'Request a flag with get_flag().\n' + \
              'Only if the 32 bit access permission bitmask in scratch flash ' \
              'storage at offset 0x0FFC-0xFFF is nonzero can you get one.\n\n' + \
              'You can access scratch via scratch.read(offset, length) and ' \
              'scratch.write(offset, data) where data is a bytestring.\n\n' + \
              'You can paste snippets using CTRL+E and CTRL+D.\n\n' + \
              'Warning: writing data refreshes an entire page.\n\n'

_message_console = _message_ui

display.drawFill(0x0)
easydraw.messageCentered('Wear and Tear\n\n\n' + _message_ui + '\n' * 5)


def help():
    print(_message_console)

help()
