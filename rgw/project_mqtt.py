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
        # 각 센서들 초기화
        self.led = LED(2)
        self.pump = WaterPump()
        self.secure = Human_Detect()
        
        # 보안 스레드 상태 관리
        self.secure_thread = None
        self.security_active = False

    # 현관 센서 호출
    def porch(self, room, message):
        if message == 'security_on':
            self.secure.start()
        elif message == 'security_off':
            self.secure.stop()
            
        # 보안 활성시 작업은 추후에

    # 거실 센서 호출
    def living_room(self, room, message):
        if message == 'led_on':
            self.led.led_on()
        elif message == 'led_off':
            self.led.led_off()
        elif message == 'pump_on':
            self.pump.pump_on(3)
        
    # 연결접속 함수
    def on_connect(self, client, userdata, flags, rc):
        print("connect..."+str(rc))
        time.sleep(0.5)
        if rc==0:
            client.subscribe("/home/#")
        else:
            print("연결실패")
    
    def on_message(self, client, userdata, message):
        find_room = message.topic.split("/")
        myval = message.payload.decode("utf-8").split("/")
        print(message.topic+"===>", myval)
        print(myval[0])
        if myval[0] == 'porch':
            self.porch(find_room[1], myval[0])
        elif myval[0] == 'living':
            self.living_room(find_room[1], myval[0])

    
    def mqtt_connect(self):
        print("브로커 연결 시작")
        # self.client.connect("192.168.14.168", 1883, 60) # 창석님 IP주소
        self.client.connect("192.168.14.39", 1883, 60) #다온님 IP주소
        
        mqtt_obj = Thread(target=self.client.loop_forever)
        mqtt_obj.start()
        try:
            mqtt_obj.join()
            
        except KeyboardInterrupt:
            pass
        finally:
            self.secure.terminate()
            gpio.cleanup()