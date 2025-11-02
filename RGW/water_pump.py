import RPi.GPIO as gpio
import time

class WaterPump:
    # 초기화
    def __init__(self):
        
        # 핀번호 설정
        self.A_1A = 19 # 모터제어 1핀
        self.A_1B = 13 # 모터제어 2핀
        
        gpio.setup(self.A_1A, gpio.OUT)
        gpio.setup(self.A_1B, gpio.OUT)
        
        gpio.output(self.A_1A, gpio.LOW)
        gpio.output(self.A_1B, gpio.LOW)
        
    # 펌프 작동
    # 모터가 총 num번 동작하며, 화분에 물을 주는 역할을 함
    # 추후에 이걸 응용해 스프링쿨러 등으로 활용 가능
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
            gpio.output(self.A_1A, gpio.LOW)
            gpio.output(self.A_1B, gpio.LOW)