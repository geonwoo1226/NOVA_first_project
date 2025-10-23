import board
import adafruit_dht
import time

class HumiTempButton:
    # 초기화
    def __init__(self, humi_temp_pin):
        self.humi_temp_pin = humi_temp_pin
        self.mydht11 = adafruit_dht.DHT11(board.D21)
        self.humidity_data = self.mydht11.humidity
        self.temperature_data = self.mydht11.temperature
        
    # 온습도 측정
    def sensor_measure(self):
        try:
            print("습도 : {}%, 온도 : {}°C".format(self.humidity_data, self.temperature_data))
            
            # 센서 내부에서 초기화작업시 필요한 시간
            time.sleep(2)
        except RuntimeError as error:
            print(error.args[0])