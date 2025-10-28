import RPi.GPIO as gpio
import time

class LED:
    # 초기화
    def __init__(self, num):
        if num == 1:
            self.led_pin = 21     # 현관 전등
        elif num == 2:
            self.led_pin = 26    # 거실 전등
        
        # 초기화
        gpio.setmode(gpio.BCM)
        gpio.setup(self.led_pin, gpio.OUT)
        
        self.button_pin = 6
        gpio.setup(self.button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        
    # led on
    def led_on(self):
        gpio.output(self.led_pin, gpio.HIGH)
        
    # led off
    def led_off(self):
        gpio.output(self.led_pin, gpio.LOW)
        
    # led 점등
    def led_switch(self):
        while True:
            if gpio.input(self.button_pin) == gpio.LOW:
                break
            self.led_on(1)
            time.sleep(0.05)
            self.led_off(1)
            time.sleep(0.05)