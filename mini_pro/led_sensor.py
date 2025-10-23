import RPi.GPIO as gpio
import time

class LED:
    # 초기화
    def __init__(self):
        self.led_pin = 26
        gpio.setmode(gpio.BCM)
        gpio.setup(self.led_pin, gpio.OUT)
        
        self.button_pin = 19
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
            self.led_on()
            time.sleep(0.05)
            self.led_off()
            time.sleep(0.05)