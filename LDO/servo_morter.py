import RPi.GPIO as gpio
import time

class ServoMorter:
    def __init__(self):
        self.servo_pin_1 = 23   # 1번방 창문
        self.servo_pin_2 = 20   # 2번방 창문
            
        # gpio 입출력모드 지정
        gpio.setup(self.servo_pin_1, gpio.OUT)
        gpio.setup(self.servo_pin_2, gpio.OUT)
        
        # 센서별 PWM 설정
        # PWM(Pulse With Modulation) - 펄스 폭 변조 : 디지털 출력으로 아날로그 회로 지어
        self.pwm_1 = gpio.PWM(self.servo_pin_1, 50)
        self.pwm_2 = gpio.PWM(self.servo_pin_2, 50)
    
    # 창문 열기
    # num = 1/2 : 1/2번방 창문
    def window_open(self, num):
        if num == 1:
            self.pwm_1.start(2.5)
            time.sleep(0.5)
            for i in range(30,126):
                self.pwm_1.ChangeDutyCycle(i/10)
                time.sleep(0.01)
        elif num == 2:
            self.pwm_2.start(2.5)
            time.sleep(0.5)
            for i in range(30,126):
                self.pwm_2.ChangeDutyCycle(i/10)
                time.sleep(0.01)

    # 창문 닫기
    # num = 1/2 : 1/2번방 창문
    def window_close(self, num):
        if num == 1:
            self.pwm_1.start(12.5)
            time.sleep(0.5)
            for i in range(125, 29, -1):
                self.pwm_1.ChangeDutyCycle(i/10)
                time.sleep(0.01)
        elif num == 2:
            self.pwm_2.start(12.5)
            time.sleep(0.5)
            for i in range(125, 29, -1):
                self.pwm_2.ChangeDutyCycle(i/10)
                time.sleep(0.01)