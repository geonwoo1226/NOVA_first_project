import RPi.GPIO as gpio
import time

class LED:
    # 초기화
    def __init__(self, led_pin):
        self.led_pin = led_pin
        gpio.setmode(gpio.BCM)
        gpio.setup(self.led_pin, gpio.OUT)
        
    # led on
    def led_on(self):
        gpio.output(self.led_pin, gpio.HIGH)
        
    # led off
    def led_off(self):
        gpio.output(self.led_pin, gpio.LOW)
        
    # led 점등
    def led_switch(self):
        gpio.output(self.led_pin, gpio.HIGH)
        time.sleep(0.05)
        gpio.output(self.led_pin, gpio.LOW)
        time.sleep(0.05)
        
    def clean(self):
        gpio.cleanup