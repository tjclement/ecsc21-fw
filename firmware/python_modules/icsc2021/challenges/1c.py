import display, easydraw, flags

def generate_token(user: str):
    import ucryptolib
    import uos
    import ubinascii as ub

    KEY = b'\x24\xf0\x7f\xb9\x62\x76\x84\xf4\x05\xa8\x70\xf0\x90\x5b\x66\x0d'
    MODE_CBC = 2
    BLOCK_SIZE = 16

    def pad(s: bytes):
        rem = BLOCK_SIZE - (len(s) % BLOCK_SIZE)

        if rem == 0:
            rem = BLOCK_SIZE

        return s + ((rem).to_bytes(1, 'big') * rem)

    if not user or not isinstance(user, str):
        print('Invalid user: name must be a non-empty string')
        return

    if len(user) > 16:
        print('Invalid user: length cannot be more than 16 characters!')
        return

    if 'root' in user.lower():
        print('Illegal user: user %s is not allowed!' % user)
        return

    token = '{user:"%s"}' % user
    token = token.encode()

    iv = uos.urandom(16)
    cipher = ucryptolib.aes(KEY, MODE_CBC, iv)

    encrypted = iv + cipher.encrypt(pad(token))
    encrypted = ub.hexlify(encrypted)
    encrypted = encrypted.decode()

    print('Secure token: %s' % encrypted)


def submit_token(token: str):
    import ucryptolib
    import ubinascii as ub

    BLOCK_SIZE = 16
    MAX_BLOCKS_TOKEN = 6
    MIN_BLOCKS_TOKEN = 2
    MAX_LEN_TOKEN = 2 * BLOCK_SIZE * MAX_BLOCKS_TOKEN 
    MIN_LEN_TOKEN = 2 * BLOCK_SIZE * MIN_BLOCKS_TOKEN

    KEY = b'\x24\xf0\x7f\xb9\x62\x76\x84\xf4\x05\xa8\x70\xf0\x90\x5b\x66\x0d'
    MODE_CBC = 2

    def unpad(s):
        padlen = s[-1]
        slen = len(s)
        if padlen > slen:
            return None
        for i in range(padlen):
            if s[slen - i - 1] != padlen:
                return None
        return s[:-padlen]

    if not isinstance(token, str):
        print('Invalid secure token: must be a string')
        return

    token_len = len(token)

    if token_len < MIN_LEN_TOKEN or token_len % (BLOCK_SIZE * 2) != 0:
        print('Invalid secure token')
        return

    if len(token) > MAX_LEN_TOKEN:
        print('Invalid secure token: longer than the maximum (%d) allowed!' % MAX_LEN_TOKEN)
        return

    try:
        token = ub.unhexlify(token)
    except:
        print('Invalid secure token: must be hex-encoded!')
        return

    iv, ciphertext = token[:16], token[16:]
    cipher = ucryptolib.aes(KEY, MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext)) or ''

    if decrypted == b'{user:"root"}':
        flag = 'CTF{%s}' % '368edff21a67bdb9ebdf9e400b82a27fff806a8e8fbd369b'
        print('Access authorized! Here\'s your flag: %s' % flag)
        flags.submit_flag(flag)
    else:
        print('Unauthorized access attempt with token: %s' % decrypted)

_message_ui = 'You may only continue if you are root.\n' + \
        'Please read the instructions in your console and '+ \
        'provide a valid token to gain access to the flag.\n\n' + \
        'You can paste snippets using CTRL+E and CTRL+D.\n\n'+ \
        'You can submit the flag by calling flags.submit_flag("CTF{xxxx}").'

_message_console = 'NOTICE: this system uses the Secure Access Token (SAT) mechanism' + \
        'which is based on the military-grade AES-CBC encryption scheme.\n' + \
        'You may get a guest access token by calling generate_token(user="username").\n' + \
        'In order to gain access to the flag, please provide a token proving that you are root\n' + \
        'by calling submit_token(token="xxxx").'

display.drawFill(0x0)
easydraw.messageCentered('Got root?\n\n\n' + _message_ui + '\n' * 13)


def help():
    print(_message_console)

help()