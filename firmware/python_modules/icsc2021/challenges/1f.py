import flags, display, easydraw


def encrypt(plaintext):
    if type(plaintext) == str:
        plaintext = plaintext.encode("ascii")
    if type(plaintext) != bytes:
        print("You can only encrypt strings or byte strings.")
        return

    plaintext = bytearray(plaintext)

    key = b"\x57\x15\x71\xd8\x3c\xee\x2e\x79\x3a\x7c\xc7\x5a\x33\x34\xfb\x00"
    key_length = len(key)
    for index, char in enumerate(plaintext):
        plaintext[index] ^= key[index % key_length]

    return bytes(plaintext)


_crypt_flag = b'\x14A7\xa3\t\x8a\x1c\x1d\\\x1d\xff;Q\r\xc32n"\x14\xbbY\xd8K\x1f^O\xf4c\x00\x05\xc3db"E\xbb\x04\xd7J\x1f\x0f\x1e\xf28\x00\x07\xce43\'F\xe1A'
_message_ui = (
    'This flag shown in your terminal was encrypted using perfect security.\n\nThe scheme is so secure, that we\'ll allow you to test it yourself by calling encrypt("yourphrase").\n\n'
    + 'You can submit the decrypted flag by calling flags.submit_flag("CTF{xxxx}").'
)

display.drawFill(0x0)
easydraw.messageCentered("One Time Pwn\n\n\n" + _message_ui)

print("Encrypted flag: ", str(_crypt_flag))
