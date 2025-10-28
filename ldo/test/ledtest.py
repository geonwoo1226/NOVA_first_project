import RPi.GPIO as GPIO
import time

led_pin = 24
#GPIO핀을 어떤 방법으로 액세스할 것인지 모드를 설정
GPIO.setmode(GPIO.BCM)

#GPIO핀이 입력 or 출력 설정
GPIO.setup(led_pin,GPIO.OUT)

#GPIO핀에 출력
GPIO.output(led_pin,GPIO.HIGH) #23번으로 HIGH(1)값을 출력
time.sleep(1)
GPIO.output(led_pin,GPIO.LOW) #23번으로 LOW(1)값을 출력

#GPIO핀 초기화
GPIO.cleanup()



