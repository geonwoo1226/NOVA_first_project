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
        
        # 센서 호출
        self.buzzer = Buzzer()
        self.led = LED()
        
        # Thread 설정
        self.led_switch = Thread(target=self.led.led_switch)
        self.kitchen_buzzer = Thread(target=self.buzzer.kitchen_buzzer)
        
    
    
    # 화재 감지시 활성화되는 함수
    def detection(self):
        
        print("화재발생")
        self.led_switch.start()
        self.kitchen_buzzer.start()
        try:
            self.led_switch.join()
            self.kitchen_buzzer.join()
            
        except KeyboardInterrupt:
            pass
        
        finally:
            print("화재경보 중지")
            self.buzzer.stop_buzzer()