import RPi.GPIO as gpio
import time

class Buzzer:
    # 초기화
    def __init__(self):
        buzzer_pin = 16
        gpio.setmode(gpio.BCM)
        gpio.setup(buzzer_pin, gpio.OUT)
        self.pwm = gpio.PWM(buzzer_pin, 1)
        
        self.button_pin = 6
        gpio.setup(self.button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        
    
    # 부엌 화재경보 작동시
    def kitchen_buzzer(self):
        while True:
            if gpio.input(self.button_pin) == gpio.LOW:
                break
            self.pwm.ChangeFrequency(932)
            self.pwm.start(50)
            time.sleep(0.1)
            self.pwm.stop()
            time.sleep(0.1)
            
    # 외출 때 사람 감지시 발생하는 소음
    def security_buzzer(self):
        while True:
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
        gpio.cleanup()
            