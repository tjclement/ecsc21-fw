import virtualtimers, time, flags, display, easydraw

virtualtimers.begin(500)


def print_flag():
    def actual_print():
        try:
            with open("/proc/uid", "rt") as file:
                uid = int(file.read())
        except:
            print(
                "Debug: /proc/uid is corrupt: does not contain textual integer user ID."
            )
            return -1
        if uid != 0:
            print("Only the root user is allowed to print the flag.")
            return -1
        else:
            print(
                "Congratulations, here's your flag: CTF{%s}"
                % "6c78629ca4bb5dc3f509e3a97744ce26e3adf1740edd4b5d"
            )
        return -1

    print("Debug: Verifying integrity of /proc/uid..")
    time.sleep(1)
    try:
        with open("/proc/uid", "rt") as file:
            uid = int(file.read())
    except:
        print("Debug: /proc/uid is corrupt: does not contain textual integer user ID.")
        return

    if uid != 1000:
        print("User ID has been tampered with! Exiting.")
        return
    else:
        print(
            "Debug: User ID integrity checks out. Yielding the processor to be sociable to other processes before printing flag.."
        )
        virtualtimers.new(500, actual_print)


_message_ui = (
    "Use print_flag() to obtain the flag. You can paste snippets using CTRL+E and CTRL+D.\n\n"
    + 'You can submit the flag by calling flags.submit_flag("CTF{xxxx}").'
)

display.drawFill(0x0)
easydraw.messageCentered("Timing is Key\n\n\n" + _message_ui)
