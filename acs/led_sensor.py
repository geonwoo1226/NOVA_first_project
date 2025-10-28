import RPi.GPIO as gpio
import time

class LED:
    # 초기화
    def __init__(self):
        # self.led_pin_firstRoom = 26
        # self.led_pin_secondRoom = 18
        self.led_pin = 6
        
        gpio.setmode(gpio.BCM)
        # gpio.setup(self.led_pin_first, gpio.OUT)
        # gpio.setup(self.led_pin_second, gpio.OUT)
        gpio.setup(self.led_pin, gpio.OUT)
        
        self.button_pin = 19
        gpio.setup(self.button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        
    # led on
    # def led_on(self, value):
    #     if value == 1:
    #         gpio.output(self.led_pin_firstRoom, gpio.HIGH)
    #     elif value == 2:
    #         gpio.output(self.led_pin_secondRoom, gpio.HIGH)
    
    def led_on(self):
        gpio.output(self.led_pin, gpio.HIGH)
        
    # led off
    # def led_off(self, value):
    #     if value == 1:
    #         gpio.output(self.led_pin_first, gpio.LOW)
    #     elif value == 2:
    #         gpio.output(self.led_pin_second, gpio.LOW)
    
    def led_off(self):
        gpio.output(self.led_pin, gpio.LOW)
        
    # led 점등
    def led_switch(self):
        while True:
            if gpio.input(self.button_pin) == gpio.LOW:
                break
            self.led_on()
            time.sleep(0.05)
            self.led_off()
            time.sleep(0.05)