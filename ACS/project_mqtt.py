import paho.mqtt.client as client
from threading import Thread
import time
import RPi.GPIO as gpio
from lcd_display import LCD_Display


class MqttWorker:
    # 초기화
    def __init__(self):
        self.client = client.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # GPIO 핀번호 참조방식 결정 - 다른 소스코드에서는 빼고 이곳에서만 사용하여 충돌 방지
        # BCM 모드 - 핀 번호를 GPIO모듈 번호로 사용
        gpio.setmode(gpio.BCM)
        
        self.lcd = LCD_Display()    # LCD관련 라이브러리 호출
        
        # publish하기위한 초기화 작업
        self.mqtt_client = client.Client()
        self.mqtt_client.connect("192.168.14.39", 1883)
    
    
    # mosquitto publish 성공 시 보내지는 메세지
    def publish_ok(client, userdata, mid):
        print(client, userdata, mid)
        print("사용자에게 메세지를 전송하였습니다.") 
    
    
    # 연결접속 함수
    def on_connect(self, client, userdata, flags, rc):
        print("connect..."+str(rc))
        self.lcd.lcd_run("MQTT", "Connect...")
        time.sleep(0.5)
        
        if rc==0:
            client.subscribe("home/#")
        else:
            print("연결실패")
    
    def on_message(self, client, userdata, message):
        # 토픽 : home/lcd
        find_lcd_topic = message.topic.split("/")

        # 방/센서
        myval = message.payload.decode("utf-8").split("/")
        print(message.topic+"===>", myval)
        room = message.topic.split("/")


        if find_lcd_topic[1] == 'lcd':
            print("lcd출력")
            self.lcd.lcd_run(myval[0], myval[1])
        else:
            pass
        
    def mqtt_connect(self):
        # 브로커 연결
        print("브로커 연결 시작")
        self.client.connect("192.168.14.39", 1883, 60)
        
        mqtt_obj = Thread(target=self.client.loop_forever)
        mqtt_obj.start()
        try:
            # 다른 Thread있으면 같이 무한대기
            mqtt_obj.join()

        # Ctrl + c 클릭 시 오류 생성 넘기기
        except KeyboardInterrupt:
            pass
        
        # 전체 센서 초기화
        # 다른 클래스에서는 제거해두고 이곳에서만 초기화 작업
        finally:
            self.lcd.lcd_byte(0x01, self.lcd.LCD_CMD)
            self.lcd.bus.close()
            gpio.cleanup()