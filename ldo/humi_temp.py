import board
import adafruit_dht
import time
from threading import Thread
import RPi.GPIO as gpio

from led import LED
from buzzer import Buzzer

class HumiTempButton:
    # 초기화
    def __init__(self):
        # 핀번호 고정부여 / 온습도값 부여
        
        #버튼 초기화
        self.button_pin = 12
        gpio.setup(self.button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        
        self.buzzer = Buzzer()
        self.led = LED()
    
    # 온습도 1회 측정 - 1마다 한번씩 측정해 측정 후 10초동안 받아와 평균을 출력
    # def one_measure(self):
    #     try:
    #         sum_hu = 0
    #         sum_temp = 0
    #         print("측정을 시작합니다.")
    #         time.sleep(0.5)
    #         print("측정중...")
    #         for i in range(10):
    #             sum_hu += self.humidity_data
    #             sum_temp += self.temperature_data
    #             time.sleep(1)
    #         time.sleep(0.3)
    #         print("측정이 완료되었습니다.")
    #         print("습도 : {:.2f}%, 온도 : {:.2f}°C".format(sum_hu/10, sum_temp/10))
    #     except RuntimeError as error:
    #         print(error.args[0])
    
    # 화재 감지시 활성화되는 함수
    def detection(self):
        led_switch = Thread(target=self.led.led_switch)
        kitchen_buzzer = Thread(target=self.buzzer.kitchen_buzzer)
        
        led_switch.start()
        kitchen_buzzer.start()
        try:
            print("화재발생")
            
            
            led_switch.join()
            kitchen_buzzer.join()
            
            
        finally:
            print("화재경보 중지")
            self.buzzer.stop_buzzer()