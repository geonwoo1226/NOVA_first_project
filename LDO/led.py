import RPi.GPIO as gpio
import time

class LED:
    # 초기화
    def __init__(self):
        self.led_pin_room1 = 24     # 1번방 전등
        self.led_pin_room2 = 21     # 2번방 전등
        self.led_pin_kitchen = 6    # 부엌 전등
        self.led_pin_warn = 13      # 화재경보등
        
        # gpio 입출력모드 지정
        gpio.setup(self.led_pin_room1, gpio.OUT)
        gpio.setup(self.led_pin_room2, gpio.OUT)
        gpio.setup(self.led_pin_kitchen, gpio.OUT)
        gpio.setup(self.led_pin_warn, gpio.OUT)
        
        # 화재작동시 중지시키기 위한 버튼
        self.button_pin = 12
        gpio.setup(self.button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        
        
    # led on
    def led_on(self, value):
        if value == 1:
            gpio.output(self.led_pin_room1, gpio.HIGH)
        elif value == 2:
            gpio.output(self.led_pin_room2, gpio.HIGH)
        elif value == 3:
            gpio.output(self.led_pin_kitchen, gpio.HIGH)
        elif value == 4:
            gpio.output(self.led_pin_warn, gpio.HIGH)
        
    # led off
    def led_off(self, value):
        if value == 1:
            gpio.output(self.led_pin_room1, gpio.LOW)
        elif value == 2:
            gpio.output(self.led_pin_room2, gpio.LOW)
        elif value == 3:
            gpio.output(self.led_pin_kitchen, gpio.LOW)
        elif value == 4:
            gpio.output(self.led_pin_warn, gpio.LOW)
        
    # 화재경보 점등
    def led_switch(self):
        while True:
            if gpio.input(self.button_pin) == gpio.LOW:
                break
            self.led_on(4)
            time.sleep(0.05)
            self.led_off(4)
            time.sleep(0.05)