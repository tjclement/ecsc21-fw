import machine, sys, system, time, virtualtimers
import _device as device

rtc = machine.RTC()
rtc.write(0, 0)
rtc.write(1, 0)

device.prepareForWakeup()

import orientation, display

# Set display backlight
display.drawFill(0x0)
display.flush()
pin = machine.PWM(2, freq=20000, duty=100)
orientation.default()
del orientation, display

__chk_recovery = False
fc_level = machine.nvs_getint("system", 'factory_checked') or 0
countdown_time = machine.nvs_getint("system", "countdown_time") or 28800  # By default start with 8 hours countdown


def countdown_tick():
    global countdown_time
    old_value = countdown_time
    countdown_time -= 1

    # Protect nvs by persisting the timer only once each 10 seconds
    if countdown_time >= 0 and countdown_time % 10 == 0:
        machine.nvs_setint("system", "countdown_time", countdown_time)

    if old_value == 1 and countdown_time == 0:
        system.reboot()

    return 1000  # Run again in 1 sec


# Application starting
app = rtc.read_string()
if not app:
    if fc_level < 4:
        app = "factory_checks"
    elif not machine.nvs_getint("system", "splash_shown"):
        machine.nvs_setint("system", "splash_shown", 1)
        app = "bootsplash"
    else:
        app = machine.nvs_getstr("system", "default_app")
        if not app:
            app = "dashboard.home"
    del fc_level

del rtc

if app and not app == "shell":
    try:
        # print("Starting app '%s'..." % app)
        system.__current_app__ = app
        if app:
            module = __import__(app)
            parts = app.split(".")
            for submodule in parts[1:]:
                module = getattr(module, submodule)
            # Expose the started module's properties as globals, so
            # users can approach them via the python console
            for name in dir(module):
                globals()[name] = getattr(module, name)

            # Run update_countdown here so regardless of being in the menu or a challenge
            # the timer continues
            virtualtimers.begin(100)
            if not machine.nvs_getint('system', 'ctf_done'):
                virtualtimers.new(0, countdown_tick)
    except KeyboardInterrupt:
        system.launcher()
    except BaseException as e:
        sys.print_exception(e)
        if not machine.nvs_get_u8("system", "ignore_crash"):
            print("Fatal exception in the running app!")
            system.crashedWarning()
            time.sleep(3)
            system.launcher()
