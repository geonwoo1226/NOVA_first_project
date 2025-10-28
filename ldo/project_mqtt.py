import paho.mqtt.client as client
from threading import Thread
import time
import RPi.GPIO as gpio
from led import LED
from lcd_temp import LCD_Temp
from servo_morter import ServoMorter


class MqttWorker:
    def __init__(self):
        self.client = client.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        gpio.setmode(gpio.BCM)

        self.led = LED()
        self.lcd_temp = LCD_Temp()
        self.windows_1 = ServoMorter(1)
        self.windows_2 = ServoMorter(2)

        # 호실과 구역 리스트 설정
        self.room = ['3001', '3002', '5001', '5002']
        self.room_name = ['거실', '현관', '부엌']

    # 방1 센서 호출
    def room1(self, room, message):
        if message == 'led_on':
            self.led.led_on(1)
        elif message == 'led_off':
            self.led.led_off(1)
        elif message == 'window_open':
            self.windows.window_open(1)
        elif message == 'window_close':
            self.windows.window_close(1)

    # 방2 센서 호출
    def room2(self, room, message):
        if message == 'led_on':
            self.led.led_on(2)
        elif message == 'led_off':
            self.led.led_off(2)
        elif message == 'window_open':
            self.windows.window_open(2)
        elif message == 'window_close':
            self.windows.window_close(2)

    # 부엌 센서 호출
    def kitchen(self, room, message):
        if message == 'led_on':
            self.led.led_on(3)
        elif message == 'led_off':
            self.led.led_off(3)
        
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

        if myval[0] == '방1':
            print()
        elif myval[0] == '방2':
            print()
        elif myval[0] == '부엌':
            print()
    
    def mqtt_connect(self):
        lcd_temp = Thread(target=self.lcd_temp.lcd_run)
        mqtt_obj = Thread(target=self.client.loop_forever)
        try:
            print("브로커 연결 시작")
            # self.client.connect("192.168.14.168", 1883, 60) # 창석님 IP주소
            self.client.connect("192.168.14.39", 1883, 60) #다온님 IP주소
            
            mqtt_obj.start()
            
            time.sleep(3)
            print("온습도센서 작동시작")
            lcd_temp.start()
            
            print("testset")

            # 다른 Thread있으면 대기
            mqtt_obj.join()
            lcd_temp.join()

        except Exception as e:
            print("에러 : " +e)
        finally:
            gpio.cleanup()
            