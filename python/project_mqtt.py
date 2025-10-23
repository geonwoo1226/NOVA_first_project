import paho.mqtt.client as client
import RPi.GPIO as gpio
from threading import Thread
import time

class MqttWorker:
    def __init__(self):
        self.client = client.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    # 연결접속 함수
    def on_connect(self, client, userdata, flag, rc):
        print("connect..."+str(rc))
        time.sleep(0.5)
        if rc==0:
            client.subscribe("home/#")
        else:
            print("연결실패")
    
    
    
    def mqtt_connect(self):
        try:
            print("브로커 연결 시작")
            self.client.connect("192.168.14.168", 1883, 60)
            
            mqtt_obj = Thread(target=self.client.loop_forever)
            mqtt_obj.start()
        except KeyboardInterrupt:
            pass
        finally:
            print("종료")