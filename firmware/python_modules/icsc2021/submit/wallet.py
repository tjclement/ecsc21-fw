import flags, easydraw, time

_message = "We need to know how Zagan handles their finances in the underground. Please help us find the address of their bitcoin wallet. You can submit it to us here via the terminal."

print(_message)
easydraw.messageCentered("Zagan's Bitcoin Wallet\n\n\n" + _message)


def check():
    while True:
        wallet = input("Bitcoin wallet address: ")
        time.sleep(2)
        if wallet == "14ocYc2N3TG4oxZEnx8te76NCuhTdySPzJ":
            print("Another job well done, congratulations. We'll add a flag for you as a token of your efforts.")
            flags.submit_flag("CTF{%s}" % "3f760b3a9eadc00b29de09c405d0b0d5ba2459efc3ea52d8")
            break
        else:
            print("Our systems indicate that this address is invalid or not likely associated with the Sixth Circle.")


check()
