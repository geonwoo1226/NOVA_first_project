import RPi.GPIO as GPIO
import time
from buzzer import Buzzer
from led_sensor import LED
from threading import Thread


# 핀 번호 설정 (BCM 모드)
GPIO.setmode(GPIO.BCM)

# PIR 센서 핀
PIR_PIN = 12
GPIO.setup(PIR_PIN, GPIO.IN)

# 초음파 센서 핀
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# 다른센서 호출 및 초기화
led = LED()
buzzer = Buzzer()

print("PIR + 초음파 센서 실습 시작 (Ctrl + C 로 종료)")

def measure_distance():
    GPIO.setmode(GPIO.BCM)
    """초음파 센서로 거리 측정 (cm 단위 반환)"""
    # 트리거 핀을 잠시 HIGH로
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Echo 신호 대기
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # 거리 계산
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # (음속 34300cm/s ÷ 2)
    distance = round(distance, 2)
    return distance

led_switch = Thread(target=led.led_switch)
secu_buzzer = Thread(target=buzzer.security_buzzer)

print("측정을 시작합니다...")
time.sleep(3)
while True:
    distance = measure_distance()
    if GPIO.input(PIR_PIN) == 1 and distance < 100:  # 인체 감지됨
        print("인체 감지됨! 거리 측정 중...")
        print(f"측정된 거리: {distance} cm\n")
        led_switch.start()
        secu_buzzer.start()
        try:
            led_switch.join()
            secu_buzzer.join()
        finally:
            buzzer.stop_buzzer()
            break
    else:
        print("감지 없음")
    time.sleep(0.5)

