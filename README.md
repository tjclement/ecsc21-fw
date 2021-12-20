# New badge.team ESP32 Firmware

This repository contains the reworked firmware platform for generic ESP32-based hardware devices.

badge.team firmware has been used by many event badges, such as:
* SHA2017
* HackerHotel 2019
* Disobey 2019
* CampZone 2019
 
<!--# Resources

* [Project documentation](https://wiki.badge.team)
* [Documentation](https://wiki.badge.team/Firmware)
* [Firmware](https://github.com/badgeteam/ESP32-Firmware)
* [Changelog](CHANGELOG.md)


[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a61bf7ca8c6040e78382af2741a67d04)](https://www.codacy.com/app/Badgeteam/ESP32-Firmware?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=badgeteam/ESP32-Firmware&amp;utm_campaign=Badge.team)
[![Build Status](https://travis-ci.org/badgeteam/ESP32-Firmware.svg?branch=master)](https://travis-ci.org/badgeteam/ESP32-Firmware)
-->

## Debian prerequisites

```
sudo apt-get install make unzip git libncurses5-dev flex bison gperf python-serial libffi-dev libsdl2-dev libmbedtls-dev perl
```

## Mac prerequisites
```bash
brew install python3
pip3 install -r requirements.txt
```

## Preparing your setup

First, make sure you pull the submodules in the project:

```
git submodule update --init --recursive
```

Next, copy the xtensa build toolchain for your OS (currently supporting Linux and Mac OS) from /toolchains/, and unpack and save it as /xtensa-esp32-elf/ in the project root folder:

For linux:
```
unzip -p toolchain/xtensa-esp32-elf-linux64.zip xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar | tar xv
```

For mac: 
```
unzip toolchain/xtensa-esp32-elf-mac.zip
```

# Selecting a specific existing badge
Copy the relevant config file from `/firmware/configs/<badge>_defconfig` to `/firmware/sdkconfig`:

```
cp firmware/configs/icsc22_defconfig firmware/sdkconfig
```

# Build instructions
To build and flash the firmware belonging to the config you just copied over:
```
./build.sh (once)
./flash.sh (every time after, also does an incremental build)
```

# Important firmware locations
Python code:
```
firmware/python_modules/<badge_name>/
```
Upon boot, from that folder first ```_boot.py``` is executed, and then ```_boot.py```. Apps start by rebooting the badge with a flag to launch a particular app. If no app is set, ```dashboard/home.py``` is started.

C modules: see https://docs.badge.team/esp32-firmware-development/adding-support/drivers/

# Interacting via web interface (webserial)
In Chrome, open https://webserial.curious.supplies/

# Interacting via serial command line
By default, the badge.team firmware activates a simple python shell or serial menu after booting. You can interact with it by running:
```
./monitor.sh
```

# Python API docs:
Mostly on https://docs.badge.team/esp32-app-development/api-reference/, except for ```easydraw``` (which is used to render to the screen).

# License and information

Copyright (C) 2017-2021 BADGE.TEAM

Uses the [Micropython port for ESP32 by Loboris](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo)

Uses ESP-IDF by Espressif
