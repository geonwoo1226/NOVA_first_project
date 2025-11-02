import RPi.GPIO as gpio
import time

class Buzzer:
    # 초기화
    def __init__(self):
        buzzer_pin = 16 # 부저 핀 부여
        gpio.setup(buzzer_pin, gpio.OUT)
        self.pwm = gpio.PWM(buzzer_pin, 1)
        
        self.button_pin = 6 # 버튼 핀 부여
        gpio.setup(self.button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        
            
    # 외출 때 사람 감지시 발생하는 소음
    def security_buzzer(self):
        # 무한반복
        while True:
            # 버튼을 누르면 반복문 빠져나오게
            if gpio.input(self.button_pin) == gpio.LOW:
                break
            self.pwm.ChangeFrequency(147)
            self.pwm.start(50)
            time.sleep(0.5)
            self.pwm.stop()
            time.sleep(0.5)

    # 부저실행 종료
    def stop_buzzer(self):
        self.pwm.stop()
            