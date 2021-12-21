import flags, display, easydraw, time


def print_flag(password):
    if password is None:
        print("A password is required to print the flag.")
        return
    elif type(password) != str:
        print("Pass the password as a string.")
        return

    _pass = "d41d8cd98f00b204"
    if len(_pass) != len(password):
        print("Error: password length mismatch")
        return

    start = time.time()
    for index, char in enumerate(_pass):
        if char != password[index]:
            print("Password is incorrect.")
            print("Perf: check took %f seconds" % (time.time() - start))
            return
        else:
            time.sleep(0.01)

    print("Correct! Here's your flag: CTF{%s}" % "6f460ca38cb5fced8abeac2418b93190496de90d81c5534c")


_message_ui = (
    'Use print_flag(password="XXXXX") to obtain the flag. You can paste snippets using CTRL+E and CTRL+D.\n\n'
    + 'You can submit the flag by calling flags.submit_flag("CTF{xxxx}").'
)

display.drawFill(0x0)
easydraw.messageCentered("Sailing in Side Channels\n\n\n" + _message_ui)
