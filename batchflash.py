#!/usr/bin/env python3
import sys, threading, time
import subprocess
from os import system
from os.path import exists
import random

import serial


def find_device(number):
    devices = ['/dev/ttyUSB%d' % number,
               '/dev/ttyACM%d' % number,
               '/dev/tty.usbserial-14%d0' % number,
               '/dev/tty.usbmodem123456%d' % number,
               '/dev/tty.usbmodem%d' % number,
               '/dev/tty.usbmodem1%d' % number,
               '/dev/tty.usbmodem2%d' % number,
               '/dev/tty.usbmodem3%d' % number,
               '/dev/tty.usbmodem4%d' % number,
               '/dev/tty.usbmodem5%d' % number,
               '/dev/tty.usbmodem6%d' % number,
               '/dev/tty.usbmodem7%d' % number,
               '/dev/tty.usbmodem8%d' % number,
               '/dev/tty.usbmodem9%d' % number,
               '/dev/tty.usbmodem123456%d' % number]
    for device in devices:
        if exists(device):
            return device
    return None


def flash_daemon(number):
    print('Starting flash thread for %s' % number)
    sys.stdout.flush()
    while True:
        device = find_device(number)
        if device is not None:
            print('Flashing %s' % device)
            sys.stdout.flush()
            # cmd = 'esptool.py -p %s erase_flash && esptool.py -p %s --baud 1000000 write_flash 0x1e1000 initial_fs.zip 0xd000 ota_data_initial.bin 0x1000 bootloader.bin 0x10000 firmware.bin 0x8000 campzone2020_16MB.bin' % (
            # device, device)
            cmd = './erase.sh && ./flash.sh'
            if system(cmd) != 0:
                print('Failed to flash device')
                continue

            conn = serial.Serial(device, baudrate=115200)
            with open('factory_setup.py', 'rt') as file:
                print('Waiting for console to come up')
                conn.timeout = 0.5
                conn.write(b'\r\n'*5)  # Ctrl C
                line = b''
                while b'>>> ' not in line:
                    line = conn.readline()
                    print('Got:', line.decode('ascii'))
                    conn.write(b'\r\n')  # Ctrl C
                print('Writing config')
                conn.timeout = 10

                keys = [32387328622881569473144680951379310282, 43480789781117900751121417390164453232, 30054877397176177747563915977497147746, 3402895537065818926498636422633754747, 34107697395012075037521429754401212649, 28187990370088040439914347120584026722]
                key_index = random.randrange(0, len(keys))
                conn.write(('machine.nvs_setstr("system", "emergency_key", ("#' + str(key_index) + ' - '+str(keys[key_index])+'"))\r\n').encode('ascii'))

                conn.write(b'\x05' + file.read().encode('ascii') + b'\x04')  # CTRL E + file + CTRL D
                print('Done')


            # Give system time to adjust
            time.sleep(1)

            # Wait for device to detach
            while exists(device):
                time.sleep(0.1)

        time.sleep(0.1)


threads = [threading.Thread(target=flash_daemon, args=(i,)) for i in range(10)]
[t.start() for t in threads]
[t.join() for t in threads]
