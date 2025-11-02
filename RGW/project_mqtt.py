import paho.mqtt.client as client
from threading import Thread
import time
import RPi.GPIO as gpio
from led_sensor import LED
from water_pump import WaterPump
from human_detect import Human_Detect

class MqttWorker:
    def __init__(self):
        self.client = client.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # mqtt실행할 때 setmode설정
        gpio.setmode(gpio.BCM)
        
        # 각 센서들 초기화
        self.led = LED()
        self.pump = WaterPump()
        self.secure = Human_Detect()
        
        # 보안 스레드 상태 관리
        self.secure_thread = None
        self.security_active = False
        
    
    # 거실 센서 호출
    def living_room(self, room, message):
        if room == '5001':# 201동 5001호 를 메인으로
            if message == 'led_on':
                self.led.led_on(2)
            elif message == 'led_off':
                self.led.led_off(2)
            elif message == 'pump_on':
                self.pump.pump_on(3)
        else: # 그 이외 것들
            if message == 'led_on':
                self.led.led_on(2)
            elif message == 'led_off':
                self.led.led_off(2)
            elif message == 'pump_on':
                self.pump.pump_on(3)
    
    
    # 현관 센서 호출
    def porch(self, room, message):
        if room == '5001':
            if message == 'security_on':
                self.secure.start()
            elif message == 'security_off':
                self.secure.stop()
    
    
    # 방 별 호출되는 함수 적용
    # 3:거실, 4:현관
    def call_by_room(self, room, room_name, sensor):
        if room_name == 'living':
            self.living_room(room, sensor)
        elif room_name == 'porch':
            self.porch(room, sensor)
    
    
    # 연결접속 함수
    def on_connect(self, client, userdata, flags, rc):
        print("connect..."+str(rc))
        time.sleep(0.5)
        if rc==0:
            client.subscribe("home/#")
        else:
            print("연결실패")
    
    
    def on_message(self, client, userdata, message):
        find_room = message.topic.split("/")
        myval = message.payload.decode("utf-8").split("/")
        print(message.topic+"===>", myval)

        if find_room[1] == '201' and find_room[2] == '5001':
            if myval[0] == 'security_on':
                print("보안이 활성화되었습니다.")
                self.secure.start()
            elif myval[0] == 'security_off':
                print("보안이 해제됩니다.")
                self.secure.stop()
            elif myval[0] == 'living':
                print("진입성공2")
                self.living_room(find_room[2], myval[1])
        elif find_room[1] == 'warning' or find_room[1] == 'lcd':
            pass
        else:
            print("동호수 잘못입력")
    
    def mqtt_connect(self):
        print("브로커 연결 시작")
        self.client.connect("192.168.14.39", 1883, 60)
        
        mqtt_obj = Thread(target=self.client.loop_forever)
        mqtt_obj.start()
        try:
            mqtt_obj.join()
            
        except KeyboardInterrupt:
            pass
        finally:
            # mqtt 접속 종료 시 모든 센서 및 사용 라이브러리 초기화
            self.secure.terminate()
            gpio.cleanup()