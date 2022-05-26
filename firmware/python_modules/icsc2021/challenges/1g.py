import flags, easydraw, time
from esp32 import ULP
from machine import set_wifi_calib, deepsleep, Pin
from esp32_ulp import src_to_binary

def exec_ulp(assembly):
    # solution = """\
    # # constants from:
    # # https://github.com/espressif/esp-idf/blob/1cb31e5/components/soc/esp32/include/soc/soc.h
    # #define DR_REG_RTCCNTL_BASE          0x3ff48000
    # #define DR_REG_RTCIO_BASE            0x3ff48400
    # # constants from:
    # # https://github.com/espressif/esp-idf/blob/1cb31e5/components/soc/esp32/include/soc/rtc_io_reg.h
    # #define RTC_IO_TOUCH_PAD2_REG        (DR_REG_RTCIO_BASE + 0x9c)
    # #define RTC_IO_TOUCH_PAD2_MUX_SEL_M  (BIT(19))
    # #define RTC_GPIO_OUT_REG             (DR_REG_RTCIO_BASE + 0x0)
    # #define RTC_GPIO_ENABLE_W1TS_REG     (DR_REG_RTCIO_BASE + 0x10)
    # #define RTC_GPIO_ENABLE_W1TC_REG     (DR_REG_RTCIO_BASE + 0x14)
    # #define RTC_GPIO_ENABLE_W1TS_S       14
    # #define RTC_GPIO_ENABLE_W1TC_S       14
    # #define RTC_GPIO_OUT_DATA_S          14
    # # constants from:
    # # https://github.com/espressif/esp-idf/blob/1cb31e5/components/soc/esp32/include/soc/rtc_io_channel.h
    # #define RTCIO_GPIO2_CHANNEL          12
    # # constants from:
    # # https://github.com/espressif/esp-idf/blob/master/components/soc/esp32/include/soc/rtc_cntl_reg.h
    # #define RTC_CNTL_STATE0_REG          (DR_REG_RTCCNTL_BASE + 0x18)
    # #define RTC_CNTL_ULP_CP_SLP_TIMER_EN  (BIT(24))
    # # When accessed from the RTC module (ULP) GPIOs need to be addressed by their channel number
    # .set gpio, RTCIO_GPIO2_CHANNEL
    # .set addr_offset, 1984
    # .set wait_cycles, 800 # (8MHz / 9600 baud) minus ~30 clock cycles used for instructions in [one/zero + wait]
    # .text
    # data_addr: .long 1984 #0x50001F00 in 4-byte words, starting from 0x50000000
    # .global entry
    # entry:
    # # connect GPIO to ULP (0: GPIO connected to digital GPIO module, 1: GPIO connected to analog RTC module)
    # WRITE_RTC_REG(RTC_IO_TOUCH_PAD2_REG, RTC_IO_TOUCH_PAD2_MUX_SEL_M, 1, 1)
    # # GPIO shall be output, not input
    # WRITE_RTC_REG(RTC_GPIO_OUT_REG, RTC_GPIO_OUT_DATA_S + gpio, 1, 1)
    # load_word:
    # stage_rst
    # stage_inc 8 # Start with 8th (MSB) bit
    # move r1, data_addr
    # ld r1, r1, 0 # load address
    # ld r1, r1, 0 # load value at address
    # start_word:
    # WRITE_RTC_REG(RTC_GPIO_ENABLE_W1TC_REG, RTC_GPIO_ENABLE_W1TC_S + gpio, 1, 1)
    # wait wait_cycles
    # check:
    # # do the stuff
    # and r0, r1, 0x01
    # jumpr zero, 0, eq
    # one:
    # # turn on led (set GPIO)
    # WRITE_RTC_REG(RTC_GPIO_ENABLE_W1TS_REG, RTC_GPIO_ENABLE_W1TS_S + gpio, 1, 1)
    # jump wait
    # zero:
    # # turn off led (clear GPIO)
    # WRITE_RTC_REG(RTC_GPIO_ENABLE_W1TC_REG, RTC_GPIO_ENABLE_W1TC_S + gpio, 1, 1)
    # wait:
    # wait wait_cycles
    # rsh r1, r1, 1  # take next bit
    # # decrement stage
    # stage_dec 1
    # jumps check, 0, gt
    # end_word:
    # # turn on led (set GPIO)
    # WRITE_RTC_REG(RTC_GPIO_ENABLE_W1TS_REG, RTC_GPIO_ENABLE_W1TS_S + gpio, 1, 1)
    # wait wait_cycles
    # wait wait_cycles
    # # Next word
    # move r1, data_addr
    # ld r2, r1, 0 # load address
    # add r0, r2, 1 # increment address
    # st r0, r1, 0 # store address
    # jumpr entry, 0x1FFF, lt
    # reset:
    # move r1, addr_offset
    # move r2, data_addr
    # st r1, r2, 0
    # jump entry
    # exit:
    # halt  # go back to sleep until next wakeup period
    # """

    if not isinstance(assembly, str) or len(assembly) == 0:
        raise ValueError("assembly parameter should be a string containing assembly code")

    print("Compiling ULP assembly..")
    ulp = ULP()
    binary = src_to_binary(assembly)

    print("Starting ULP and disabling main ESP32 cores..")
    time.sleep(0.1)
    load_addr, entry_addr = 0, 8
    ulp.load_binary(load_addr, binary)

    # Disable ESP_TX output so it can be used to dump BL_EN via serial
    Pin(1, Pin.IN, Pin.PULL_FLOAT)

    flag = 'CTF{%s}' % '536dfe1422fb6620a26d2f51acadaf9fa5197239b5989e40'
    for index, char in enumerate(flag):
        # set_wifi_calib is an obfuscated primitive to write to memory
        set_wifi_calib(0x50001F00 + (index*4), ord(char))

    ulp.run(entry_addr)
    deepsleep(0)


_message_ui = (
    "Compile and execute assembly on the ULP co-processor using exec_ulp(<assembly>).\n"
    "When your ULP program runs, the flag lives at 0x50001F00, with 1 ASCII char in the LSB of every 4 bytes.\n"
    "Assembly should be sent as a multiline string of micropython-esp32-ulp assembly.\n\n"
    "You can paste snippets using CTRL+E and CTRL+D.\n"
    "You can submit the flag by calling flags.submit_flag('CTF{xxxx}')."
)

_message_console = _message_ui + \
                   "\n\nExample usage: exec_ulp(\"\"\"\\\n.text\n.global entry\nentry:\n  halt\n\"\"\")" + \
                   "\n\nscreen backlight=GPIO2=RTC_GPIO12=BL_EN=TP4\nlogo LED=GPIO15=RTC_GPIO13=right pad of R26\n" + \
                   "ESP_TX=GPIO1=bottom pad of R19\n"

print(_message_console)
easydraw.messageCentered("Eccentric Exfiltration\n\n\n" + _message_ui)
