print("Welcome to the shell of your ESP32 device!")
print("Type 'import menu' to enter the menu.")

import display
display.orientation(270)
display.backlight(0)
# display.drawFill(0x0)
# display.drawText(30, 10, "Hello world!", 0x0ffffff, "permanentmarker22")
display.drawPng(0,0,'hacker2.png')
display.flush()

import machine, time
pin=machine.PWM(2, freq=40000, duty=100)
pin2=machine.PWM(15, freq=40000, duty=0)

# while True:
#     for i in range(100):
#         pin2.duty(i)
#         time.sleep(0.01)
#     for i in range(100, 0, -1):
#         pin2.duty(i)
#         time.sleep(0.01)