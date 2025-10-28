import time
import board
import adafruit_dht

# DHT11 센서 객체 생성 (GPIO26 사용)
dht11 = adafruit_dht.DHT11(board.D26)

print("온습도 센서 테스트 시작 (Ctrl+C로 종료)")

try:
    while True:
        try:
            temperature = dht11.temperature  # 온도(섭씨)
            humidity = dht11.humidity        # 습도(%)
            
            if temperature is not None and humidity is not None:
                print(f"온도: {temperature:.1f}°C, 습도: {humidity:.1f}%")
            else:
                print("센서 데이터 읽기 실패")

        except RuntimeError as e:
            # DHT 센서 특성상 간헐적 오류가 발생할 수 있음
            print(f"오류 발생: {e.args[0]}")

        time.sleep(2)

except KeyboardInterrupt:
    print("\n프로그램 종료")
    dht11.exit()