import paho.mqtt.client as client
from threading import Thread
import time

from led_sensor import LED

class MqttWorker:
    def __init__(self):
        self.client = client.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        self.led = LED()
        
    # 연결접속 함수
    def on_connect(self, client, userdata, flags, rc):
        print("connect..."+str(rc))
        time.sleep(0.5)
        if rc==0:
            client.subscribe("home/#")
        else:
            print("연결실패")
    
    def on_message(self, client, userdata, message):
        myval = message.payload.decode("utf-8").split(":")
        print(message.topic+"===>", myval)
       
        # 테스트코드 
        # data = myval[0]
        # if data == "led_on":
        #     self.led.led_on()
        # elif data == "led_off":
        #     self.led.led_off()
    
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