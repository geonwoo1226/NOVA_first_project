import RPi.GPIO as gpio
import time

class Buzzer:
    # 초기화
    def __init__(self, buzzer_pin, button_pin):
        self.buzzer_pin = buzzer_pin
        gpio.setmode(gpio.BCM)
        gpio.setup(self.buzzer_pin, gpio.OUT)
        self.pwm = gpio.PWM(self.buzzer_pin, 1)
        
        self.button_pin = button_pin
        gpio.setup(self.button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        
    
    # 부엌 화재경보 작동시
    def kitchen_buzzer(self):
        self.pwm.ChangeFrequency(932)
        self.pwm.start(50)
        time.sleep(0.1)
        self.pwm.stop()
        time.sleep(0.1)
        
    # 외출 때 사람 감지시 발생하는 소음
    def security_buzzer(self):
        self.pwm.ChangeFrequency(147)
        self.pwm.start(50)
        time.sleep(0.5)
        self.pwm.stop()
        time.sleep(0.5)

    # 부저실행 종료
    def stop_buzzer(self):
        print("경고 종료")
        self.pwm.stop()
        self.buzzer_pin.stop_buzzer()
            

if __name__ == "__main__":
    print("기능선택")
    choice = int(input("1. 부엌, 2. 현관"))
    buzzer = Buzzer(22, 19)
    try:
        while True:
            if gpio.input(buzzer.button_pin) == gpio.LOW:
                buzzer.stop_buzzer()
                break
            
            if choice == 1:
                buzzer.kitchen_buzzer()
            elif choice == 2:
                buzzer.security_buzzer()
            else:
                print("잘못입력")
                continue
            
    finally:
        if buzzer.pwm is not None:
            buzzer.pwm.stop()
        
        gpio.cleanup()