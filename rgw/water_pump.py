import RPi.GPIO as gpio
import time

class WaterPump:
    # 초기화
    def __init__(self):
        
        # 핀번호 설정
        self.A_1A = 19 # 모터제어 1핀
        self.A_1B = 13 # 모터제어 2핀
        
        gpio.setmode(gpio.BCM)
        gpio.setup(self.A_1A, gpio.OUT)
        gpio.setup(self.A_1B, gpio.OUT)
        
        gpio.output(self.A_1A, gpio.LOW)
        gpio.output(self.A_1B, gpio.LOW)
        
    
    def pump_on(self, num):
        try:
            for i in range(num):
                #작동
                gpio.output(self.A_1A, gpio.HIGH)
                gpio.output(self.A_1B, gpio.LOW)
                time.sleep(2)
                
                #잠시 대기
                gpio.output(self.A_1A, gpio.LOW)
                gpio.output(self.A_1B, gpio.LOW)
                time.sleep(1)
        finally:
            gpio.cleanup()