import wifi, easydraw, time, virtualtimers
import network, term, sys, machine, system

system.serialWarning()


def main():
    term.empty_lines()
    items = ["Scan for networks", "Manual SSID entry", "Return to main menu"]
    callbacks = [scan, manual, home]
    callbacks[term.menu("WiFi setup", items)]()


def home():
    system.home(True)


def scan():
    wifi.disconnect()
    term.header(True, "WiFi setup")
    print("Scanning...")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    ssid_result = sta_if.scan()
    ssid_list = []
    for ssid in ssid_result:
        ssid_list.append(ssid[0].decode("utf-8", "ignore"))
    ssid_list.append("< Back")
    option = term.menu("WiFi setup - Select a network", ssid_list)
    if option != len(ssid_list) - 1:
        password(
            ssid_result[option][0].decode("utf-8", "ignore"), ssid_result[option][4]
        )


def manual():
    term.header(True, "WiFi setup - Enter SSID")
    print("Enter the SSID for the network you want to connect to, ")
    print("or leave blank to go back. Press RETURN to continue.")
    ssid = term.prompt("SSID", 1, 5)
    if len(ssid) >= 1:
        items = [
            "WEP / WPA / WPA2",
            "Open network",
            "WPA / WPA2 Enterprise",
            "Return to main menu",
        ]
        option = term.menu("WiFi setup - Authentication method", items)
        if option == 0:
            password(ssid, 1)
        elif option == 1:
            password(ssid, 0)
        elif option == 2:
            password(ssid, 5)


def password(ssidName, ssidType):
    if ssidType == 0:
        confirm(ssidName, "")
    elif ssidType == 5:
        term.header(True, "WiFi setup")
        print("WPA / WPA2 Enterprise is currently not supported!")
        print("")
        print("Press any key to return to the main menu")
        sys.stdin.read(1)
    else:
        term.header(True, "WiFi setup - Enter PASSWORD")
        print("Enter the PASSWORD for '" + ssidName + "', ")
        print("or leave blank to go back. Press RETURN to continue.")
        password = term.prompt("PASSWORD", 1, 5)
        if len(password) >= 1:
            confirm(ssidName, password)


def confirm(ssid, password):
    term.header(True, "WiFi setup")
    machine.nvs_setstr("system", "wifi.ssid", ssid)
    machine.nvs_setstr("system", "wifi.password", password)
    print("New configuration has been saved.")
    print("")
    print("SSID:\t\t" + ssid)
    if len(password) < 1:
        print("No password")
    else:
        print("PASSWORD:\t" + password)
    print("")
    print("Press any key to return to the homescreen")
    sys.stdin.read(1)
    system.home(True)


easydraw.messageCentered(
    "Firmware update\n\n\nTo update your firmware, create a WiFi hotspot with SSID badgeteam and password badgeteam, or connect to the badge via USB and configure another SSID there.\n\nAfter connecting, the badge will reboot and start updating. Please allow a few minutes for this to complete."
)


def get_wifi_settings():
    ssid = machine.nvs_getstr("system", "wifi.ssid")
    if ssid is None:
        ssid = "badgeteam"
    password = machine.nvs_getstr("system", "wifi.password")
    if password is None:
        password = "badgeteam"
    return ssid, password


is_configuring = False
wifi.connect(*get_wifi_settings())
wifi.wait(5)


def update():
    global is_configuring
    if not wifi.status():
        wifi.connect(*get_wifi_settings())
        if not is_configuring:
            wifi.wait(5)
    else:
        easydraw.messageCentered("Rebooting..\n\n")
        time.sleep(3)
        system.ota()

    return 1000


virtualtimers.begin(1000)
virtualtimers.new(0, update)

input("Press enter to configure new WiFi settings")
is_configuring = True
main()
