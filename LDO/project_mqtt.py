import paho.mqtt.client as client
from threading import Thread
import time
import RPi.GPIO as gpio
from led import LED
from lcd_temp import LCD_Temp
from servo_morter import ServoMorter


class MqttWorker:
    # 초기화
    def __init__(self):
        self.client = client.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # GPIO 핀번호 참조방식 결정 - 다른 소스코드에서는 빼고 이곳에서만 사용하여 충돌 방지
        # BCM 모드 - 핀 번호를 GPIO모듈 번호로 사용
        gpio.setmode(gpio.BCM)

        self.led = LED()                # LED관련 라이브러리 호출
        self.lcd_temp = LCD_Temp()      # LCD관련 라이브러리 호출
        self.windows = ServoMorter()    # 서보모터 라이브러리 호출
        
        # Thread 설정
        self.lcd_temp_thread = Thread(target=self.lcd_temp.lcd_on)
        self.mqtt_obj = Thread(target=self.client.loop_forever)

    # 방1 센서 호출
    # 방1 - 방 전등(LED), 창문(servo morter)
    def room1(self, message):
        if message == 'led_on':
            self.led.led_on(1)
        elif message == 'led_off':
            self.led.led_off(1)
        elif message == 'window_on':
            self.windows.window_open(1)
        elif message == 'window_off':
            self.windows.window_close(1)

    # 방2 센서 호출
    # 방2 - 방 전등(LED), 창문(servo morter)
    def room2(self, message):
        if message == 'led_on':
            self.led.led_on(2)
        elif message == 'led_off':
            self.led.led_off(2)
        elif message == 'window_on':
            self.windows.window_open(2)
        elif message == 'window_off':
            self.windows.window_close(2)

    # 부엌 센서 호출
    # 사용자 작업은 전등 on/off만
    def kitchen(self, message):
        if message == 'led_on':
            self.led.led_on(3)
        elif message == 'led_off':
            self.led.led_off(3)
        
    # 연결접속 함수
    def on_connect(self, client, userdata, flags, rc):
        print("connect..."+str(rc))
        time.sleep(0.5)
        if rc==0:
            client.subscribe("home/#")
        else:
            print("연결실패")
    
    def on_message(self, client, userdata, message):
        # topic과 message를 "/"로 구분하여 받고 split으로 나누어서 조건 부여
        find_room = message.topic.split("/")
        myval = message.payload.decode("utf-8").split("/")
        print(message.topic+"===>", myval)

        # 라즈베리파이 실제 구현을 하나의 집만 구현해놓았기 때문에 현재는 하나의 동호수 부여자만 통과
        # 201동 5001호 유저만 통과
        # 방1, 방2, 부엌만 통과
        if find_room[1] == '201' and find_room[2] == '5001':
            if myval[0] == 'room1':
                self.room1(myval[1])
            elif myval[0] == 'room2':
                self.room2(myval[1])
            elif myval[0] == 'kitchen':
                self.kitchen(myval[1])
            else:
                print("구역설정 오류")
        elif find_room[1] == 'warning' or find_room[1] == 'lcd':
            pass
        else:
            print("동호수 입력오류")
    
    def mqtt_connect(self):
        # 브로커 연결
        print("브로커 연결 시작")
        self.client.connect("192.168.14.39", 1883, 60)

        self.mqtt_obj.start()
        time.sleep(1)
        print("온습도센서 작동시작")
        self.lcd_temp_thread.start()
        try:
            # 다른 Thread있으면 같이 무한대기
            self.mqtt_obj.join()
            self.lcd_temp_thread.join()
        
        except Exception:
            pass
        
        # 전체 센서 초기화
        # 다른 클래스에서는 제거해두고 이곳에서만 초기화 작업
        finally:
            self.lcd_temp.buzzer.pwm.stop()
            self.windows.pwm_1.stop()
            self.windows.pwm_2.stop()
            gpio.cleanup()
            