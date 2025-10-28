import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

try:
    print("===================================")
    print(" RFID 태그를 리더기에 대주세요...")
    print("===================================")
    while True:
        id, text = reader.read()
        print(f"\n[RFID 감지됨]")
        print(f"카드 ID : {id}")
        print(f"카드 내용 : {text.strip() if text else '(내용 없음)'}")
        print("-----------------------------------")
        time.sleep(2)  # 2초 대기 후 다시 대기 상태로
except KeyboardInterrupt:
    print("\n종료합니다.")
finally:
    GPIO.cleanup()
