import flags, display, easydraw


def run_ulp_assembly(assembly):
    pass


_message_ui = (
    "The flag is accessible only from the ESP32's ULP co-processor.\n\n"
    "Pass (text) assembly code to run_ulp_assembly(assembly).\n\n"
    "The flag resides at offset 0xC00 in RTC SLOW memory (0x50000C00), "
    "but only whilst your ULP program is running."
    "You can submit the decrypted flag by calling flags.submit_flag("CTF{xxxx}")."
)

display.drawFill(0x0)
easydraw.messageCentered("Eccentric Exfiltration\n\n\n" + _message_ui)


