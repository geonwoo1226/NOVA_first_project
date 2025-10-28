import RPi.GPIO as gpio
import time

class ServoMorter:
    def __init__(self, num):
        if num == 1:
            self.servo_pin = 23   # 1번방 창문
        elif num == 2:
            self.servo_pin = 20   # 2번방 창문
            
        gpio.setup(self.servo_pin, gpio.OUT)
        
        self.pwm = gpio.PWM(self.servo_pin, 50)
    
    # 창문 열기
    def window_open(self):
        try:
            self.pwm.start(2.5)
            time.sleep(0.5)
            for i in range(30,126):
                self.pwm.ChangeDutyCycle(i/10)
                time.sleep(0.01)
        finally:
            self.pwm.stop()

    # 창문 닫기
    def window_close(self):
        try:
            self.pwm.start(12.5)
            time.sleep(0.5)
            for i in range(125, 29, -1):
                self.pwm.ChangeDutyCycle(i/10)
                time.sleep(0.01)
        finally:
            self.pwm.stop()