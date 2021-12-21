import flags, easydraw, time

_message = "We are interested in the personal IP address of the leader of the Sixth Circle. You can submit it to us here via the terminal."

print(_message)
easydraw.messageCentered("Zagan's Home IP\n\n\n" + _message)


def check():
    while True:
        ip = input("IP address: ")
        time.sleep(2)
        if ip == "109.235.128.209":
            print("Excellent, this helps us greatly. Good work. We'll add a flag for you as a token of your efforts.")
            flags.submit_flag("CTF{%s}" % "3f4c7476e661c43e9a2bd192e19a8cd5b48631738964d439")
            break
        else:
            print("Our systems indicate that this IP is invalid or belongs to another entity.")


check()
