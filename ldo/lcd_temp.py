import smbus2
import time
import adafruit_dht
import board
from humi_temp import HumiTempButton
import RPi.GPIO as gpio
from threading import Thread

# from led import LED
# from buzzer import Buzzer


class LCD_Temp:
    # 초기화
    def __init__(self):
        self.I2C_ADDR = 0x27  # LCD 주소 (i2cdetect로 확인)
        self.LCD_WIDTH = 16   # 문자 수 (16x2 LCD)
        self.LCD_CHR = 1
        self.LCD_CMD = 0
        
        self.LCD_LINE_1 = 0x80  # 1번째 줄 주소
        self.LCD_LINE_2 = 0xC0  # 2번째 줄 주소
        
        self.LCD_BACKLIGHT = 0x08  # 백라이트 ON
        self.ENABLE = 0b00000100   # Enable 비트
        
        # I2C 버스 객체
        self.bus = smbus2.SMBus(1)
        
        # 온습도 센서 초기화
        self.mydht11 = adafruit_dht.DHT11(board.D26)
        
        # 버튼
        self.button_pin = 12
        gpio.setup(self.button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)

        # self.led = LED()
        # self.buzzer = Buzzer()
        self.humitemp = HumiTempButton()
        
    # LCD 초기화 함수
    def lcd_init(self):
        self.lcd_byte(0x33, self.LCD_CMD)
        self.lcd_byte(0x32, self.LCD_CMD)
        self.lcd_byte(0x06, self.LCD_CMD)
        self.lcd_byte(0x0C, self.LCD_CMD)
        self.lcd_byte(0x28, self.LCD_CMD)
        self.lcd_byte(0x01, self.LCD_CMD)
        time.sleep(0.005)
        
    # Enable 펄스 주기
    def lcd_toggle_enable(self, bits):
        time.sleep(0.0005)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(0.0005)
        self.bus.write_byte(self.I2C_ADDR, (bits | ~(self.ENABLE)))
        time.sleep(0.0005)
        
    # 명령 또는 데이터 전송
    def lcd_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT

        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)
        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)
        
    # lcd에 문자열 표시
    def lcd_string(self, message, line):
        message = message.ljust(self.LCD_WIDTH, " ")
        self.lcd_byte(line, self.LCD_CMD)
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)
    
    # lcd 실행 5초동안 출력 후 초기화
    def lcd_run(self):
        while True:
            self.lcd_init()
            humi = self.mydht11.humidity
            temp = self.mydht11.temperature
            try:
                # 초기화 후 다시 출력
                self.lcd_byte(0x01, self.LCD_CMD)
                time.sleep(0.1)

                # 온도가 40도 이상이면 화재상황 작동
                if temp >= 40 :
                    cnt +=1
                    # 버튼을 누르면 경고 끄기
                    if gpio.input(self.button_pin) == gpio.LOW:
                        continue
                    # 화재발생 시 LCD에 출력되는 화면
                    # 계속 깜빡임
                    self.lcd_string("Warning !!", self.LCD_LINE_1)
                    self.lcd_string(f"Fire Break Out!", self.LCD_LINE_2)
                    time.sleep(0.5)
                    
                    self.humitemp.detection()
                    
                    self.lcd_byte(0x01, self.LCD_CMD)
                    time.sleep(0.05)
                
                # 평상시에는 온습도 측정
                self.lcd_string(f"Temp: {temp:.1f}C", self.LCD_LINE_1)
                self.lcd_string(f"Hum : {humi:.1f}%", self.LCD_LINE_2)
                print(f"온도: {temp:.1f}°C, 습도: {humi:.1f}%")
                time.sleep(1)
                self.lcd_byte(0x01, self.LCD_CMD)
                
            except Exception as e:
                print("DHT11 읽기 오류:", e)
                self.lcd_string("Read Error", self.LCD_LINE_1)
                self.lcd_string("Try again...", self.LCD_LINE_2)
        
            finally:
                self.lcd_byte(0x01, self.LCD_CMD)
                self.lcd_init()
                time.sleep(0.1)
                self.mydht11.exit()
                time.sleep(0.1)
                self.bus.close()
                time.sleep(0.5)