import RPi.GPIO as gpio
import board
import adafruit_dht
import time
from threading import Thread

from led_sensor import LED
from buzzer import Buzzer

class HumiTempButton:
    # 초기화
    def __init__(self):
        # 핀번호 고정부여 / 온습도값 부여
        mydht11 = adafruit_dht.DHT11(board.D21)
        self.humidity_data = mydht11.humidity
        self.temperature_data = mydht11.temperature
        
        #버튼 초기화
        self.button_pin = 19
        gpio.setmode(gpio.BCM)
        gpio.setup(self.button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        
        self.buzzer = Buzzer()
        self.led = LED()
        
    # 온습도 1회 측정 - 1마다 한번씩 측정해 측정 후 10초동안 받아와 평균을 출력
    def one_measure(self):
        try:
            sum_hu = 0
            sum_temp = 0
            print("측정을 시작합니다.")
            time.sleep(0.5)
            print("측정중...")
            for i in range(10):
                sum_hu += self.humidity_data
                sum_temp += self.temperature_data
                time.sleep(1)
            time.sleep(0.3)
            print("측정이 완료되었습니다.")
            print("습도 : {:.2f}%, 온도 : {:.2f}°C".format(sum_hu/10, sum_temp/10))
        except RuntimeError as error:
            print(error.args[0])
            
    # 화재 측정유무 함수
    def fire_measuere(self):
        temp_list = [2] # 이전 측정값과 현재 측정값을 비교하기 위한 리스트
        while True:
            try:
                # 이전 측정값이 없으면 [0]에 현재 측정값을 부여하고 다음 반복문 실행
                if temp_list[0] is None:
                    temp_list[0] = self.temperature_data
                    continue
                # 현재 측정값 있으면 [1]에 현재측정값 부여
                else:
                    temp_list[1] = self.temperature_data
                
                # 현재 측정값과 이전 측정값의 차이가 20 이상이면 사이렌 활성화
                if abs(temp_list[0]-temp_list[1]) >= 20 or self.temperature_data >=70:
                    self.detection()
                    break
                # 차이가 20 아래면 현재 측정값을 이전 측정값에 부여
                else:
                    temp_list[0] = temp_list[1]
                    
            except RuntimeError as error:
                print(error.args[0])
    
    
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
            