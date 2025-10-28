import RPi.GPIO as GPIO
import time

# 핀 번호 설정
AA = 19  # 모터 제어 핀 1
AB = 13  # 모터 제어 핀 2

# GPIO 모드 설정 (BCM 또는 BOARD)
GPIO.setmode(GPIO.BCM)  # BCM 번호 체계 사용
GPIO.setup(AA, GPIO.OUT)
GPIO.setup(AB, GPIO.OUT)

try:
    for i in range(3):
        # 정방향 회전
        GPIO.output(AA, GPIO.HIGH)
        GPIO.output(AB, GPIO.LOW)
        print("모터 정방향 회전 중...")
        time.sleep(2)  # 5초 유지

        # 정지
        GPIO.output(AA, GPIO.LOW)
        GPIO.output(AB, GPIO.LOW)
        print("모터 정지")
        time.sleep(5)  # 5초 유지

except KeyboardInterrupt:
    print("프로그램 종료")

finally:
    GPIO.cleanup()  # 핀 초기화
