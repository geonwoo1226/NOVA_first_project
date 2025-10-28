import RPi.GPIO as GPIO

def reset_gpio():
    try:
        GPIO.setwarnings(False)     # 경고 메시지 비활성화
        GPIO.cleanup()              # 모든 핀 초기화
        print("✅ 모든 GPIO 핀이 초기화되었습니다.")
    except Exception as e:
        print(f"⚠️ GPIO 초기화 중 오류 발생: {e}")

# 단독 실행 시
if __name__ == "__main__":
    reset_gpio()
