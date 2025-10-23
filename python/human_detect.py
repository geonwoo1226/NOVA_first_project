import RPi.GPIO as gpio
import time

class Human_Detect:
    # 초기화
    def __init__(self, choice):
        self.choice = choice # 보안 활성화(1)/비활성화(2)
        pir_pin = 5 # PIR센서핀
        
        # 초음파센서 핀
        trig = 23
        echo = 24
        
        # 센서 초기화
        gpio.setmode(gpio.BCM)
        gpio.setup(pir_pin, gpio.IN)
        gpio.setup(trig, gpio.OUT)
        gpio.setup(echo, gpio.IN)
    
    