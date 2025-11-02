# gpio.cleanup() 생략
import RPi.GPIO as gpio
import time
from buzzer import Buzzer
from led_sensor import LED
from threading import Thread

import paho.mqtt.client as client

class Human_Detect:
    # 초기화
    def __init__(self):
        # PIR센서핀
        self.pir_pin = 12
        
        # 초음파센서 핀
        self.trig = 23
        self.echo = 24
        
        # 센서 초기화
        gpio.setup(self.pir_pin, gpio.IN)
        gpio.setup(self.trig, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)
        
        # 다른센서 호출 및 초기화
        self.secu_led = LED()
        self.buzzer = Buzzer()
        
        # Thread로 만들기
        self.thread = Thread(target=self.run, daemon=True)
        self.led_switch = Thread(target=self.secu_led.led_switch)
        self.secu_buzzer = Thread(target=self.buzzer.security_buzzer)
        
        self.active = False     # 평상시엔 false, 외출시 true
        self.running = True     # 전체 스레드 종료용 플래그
        
        # publish하기위한 초기화 작업
        self.mqtt_client = client.Client()
        self.mqtt_client.connect("192.168.14.39", 1883)
        
        self.thread.start()
    
    # 초음파센서로 거리측정
    def measure_distance(self):
        # 트리거 핀을 잠시 HIGH로
        gpio.output(self.trig, True)
        time.sleep(0.00001)
        gpio.output(self.trig, False)

        # Echo 신호 대기
        while gpio.input(self.echo) == 0:
            pulse_start = time.time()

        while gpio.input(self.echo) == 1:
            pulse_end = time.time()
            
        # 거리 계산
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # (음속 34300cm/s ÷ 2)
        distance = round(distance, 2)
        return distance

    
    # 보안 활성화시 publish하기 위한 함수
    def enemy(self):
        return "Warning! Intruder Detection!"
    
    
    # publish보낸 후 확인메세지
    def publish_secu_on(self, client, userdata, mid):
        print(client, userdata, mid)
        print("사용자에게 메세지를 전송하였습니다.")  
        
    
    # 외출시 보안 활성화
    def run(self):
        cnt = True
        while self.running:
            if self.active:
                
                print("보안을 활성화합니다.")
                print("3초 후 측정을 시작합니다..")
                time.sleep(3)
                try:
                    while True:
                        distance = self.measure_distance()
                        print("측정중")
                        if gpio.input(self.pir_pin) == 1 and distance < 100:  # 인체 감지됨
                            print("인체 감지됨! 거리 측정 중...")
                            print(f"측정된 거리: {distance} cm\n")
                            
                            self.mqtt_client.on_publish = self.publish_secu_on
                            result = self.mqtt_client.publish("home/warning", "Intruder Detection")
                            print("호출결과 : ", result)
                            time.sleep(0.5)
                            
                            self.led_switch.start()
                            self.secu_buzzer.start()
                            try:
                                # 여러 개의 Thread 실행
                                self.led_switch.join()
                                self.secu_buzzer.join()
                            finally:
                                self.buzzer.stop_buzzer()
                                
                                break
                        time.sleep(0.5)
                finally:
                    print("보안을 비활성화합니다.")
                    self.stop()
            else:
                time.sleep(0.1)
        
    # 시작 함수
    def start(self):
        self.active = True
        
    # 멈추는 함수
    def stop(self):
        self.active = False
    
    # 완전종료
    def terminate(self):
        self.running = False
        self.active = False