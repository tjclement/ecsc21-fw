import flags, easydraw, efuse, binascii


def secure_read_efuse_block(block, start_offset, length):
    if block == efuse.EFUSE_BLK2 and length > 0:
        print("No access allowed to secure efuse region!")
    else:
        length = length if length > 0 else 256
        return efuse.read_block(block, start_offset, length)


def get_flag(bytes):
    """
    *** SOLUTION ***

    1.  Use the logic flaw in `secure_read_efuse_block()` to bypass the 'security'
        by providing the right block and offset with a length of 0:

    >>> secure_read_efuse_block(efuse.EFUSE_BLK2, 0, 0)
    b'P\xd1\xf7\xf8\xcb]\xe7e\xcc\x0e\x91\n\x90\x8b\xa4\x82*\x08^\xf8I\x1d\x1f\xee\x00\x00\x00\x00\x00\x00\x00\x00'
    >>> get_flag(b'P\xd1\xf7\xf8\xcb]\xe7e\xcc\x0e\x91\n\x90\x8b\xa4\x82*\x08^\xf8I\x1d\x1f\xee')
    CTF{50d1f7f8cb5de765cc0e910a908ba4822a085ef8491d1fee}

    2.  Find out that the underlying call to `efuse.read_block()` can be used directly:

    >>> efuse.read_block(efuse.EFUSE_BLK2, 0, 256)
    b'P\xd1\xf7\xf8\xcb]\xe7e\xcc\x0e\x91\n\x90\x8b\xa4\x82*\x08^\xf8I\x1d\x1f\xee\x00\x00\x00\x00\x00\x00\x00\x00'
    >>> get_flag(b'P\xd1\xf7\xf8\xcb]\xe7e\xcc\x0e\x91\n\x90\x8b\xa4\x82*\x08^\xf8I\x1d\x1f\xee')
    CTF{50d1f7f8cb5de765cc0e910a908ba4822a085ef8491d1fee}
    """
    if len(bytes) != 24:
        print("That's not valid flag data, a flag consists of 24 bytes.")
    else:
        print("CTF{%s}" % str(binascii.hexlify(bytes), "ascii"))


_message_ui = (
    "Connect to the device via USB at baud 115200. You're now in a Python shell.\n"
    "You can paste snippets using CTRL+E and CTRL+D.\n\n"
    "Extract the flag from efuse by calling secure_read_efuse_block(<block>, <start_offset>, <length>)\n"
    "Use get_flag(<bytes>) to convert found data into a flag.\n\n"
    "You can submit the flag by calling flags.submit_flag(\"CTF{xxxx}\").\n\n"
    "Run help() to repeat challenge info."
)

_message_console = (
    _message_ui + "\n\n"
    "To show off our 1337 skills we have included part of the implementation here:\n"
    """
    def secure_read_efuse_block(block, start_offset, length):
        if block == efuse.EFUSE_BLK2 and length > 0:
            print('No access allowed to secure efuse region!')
        else:
            length = length if length > 0 else 256
    """
)

def help():
    print(_message_console)

help()
easydraw.messageCentered("You shall not pass\n\n\n" + _message_ui)
