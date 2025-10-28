import smbus2
import time
import adafruit_dht
import board
import RPi.GPIO as gpio
from led import LED
from buzzer import Buzzer
from threading import Thread

# LCD1602 I2C 설정
I2C_ADDR = 0x27   # I2C 주소 (모듈에 따라 0x3F일 수도 있음)
LCD_WIDTH = 16    # 문자 수
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
ENABLE = 0b00000100

E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus2.SMBus(1)

button_pin = 12
gpio.setup(button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)

buzzer = Buzzer()
led = LED()

# LCD 초기화 함수
def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    high = mode | (bits & 0xF0) | 0x08
    low = mode | ((bits << 4) & 0xF0) | 0x08
    bus.write_byte(I2C_ADDR, high)
    lcd_toggle_enable(high)
    bus.write_byte(I2C_ADDR, low)
    lcd_toggle_enable(low)

def lcd_toggle_enable(bits):
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)

def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

def detection():
    led_switch = Thread(target=led.led_switch)
    kit_buzzer = Thread(target=buzzer.kitchen_buzzer)
    
    led_switch.start()
    kit_buzzer.start()
    try:
        led_switch.join()
        kit_buzzer.join()
    finally:
        print("화재경보 중지")
        buzzer.stop_buzzer()

# DHT11 설정 (GPIO 26번)
dht_sensor = adafruit_dht.DHT11(board.D26)

# 메인 루프
try:
    lcd_init()
    while True:
        try:
            temp = dht_sensor.temperature
            hum = dht_sensor.humidity
            if gpio.input(button_pin) == gpio.LOW:
                break
            if hum >= 50:
                detection()
                lcd_byte(0x01, LCD_CMD)
                lcd_string("Warning !!", LCD_LINE_1)
                lcd_string(f"Fire Break Out!", LCD_LINE_2)
                time.sleep(0.5)
            lcd_string(f"Temp: {temp:.1f}C", LCD_LINE_1)
            lcd_string(f"Hum : {hum:.1f}%", LCD_LINE_2)
            print(f"온도: {temp:.1f}°C, 습도: {hum:.1f}%")
        except Exception as e:
            print("DHT11 읽기 오류:", e)
            lcd_string("Read Error", LCD_LINE_1)
            lcd_string("Try again...", LCD_LINE_2)

        time.sleep(1)

finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!", LCD_LINE_1)
    time.sleep(1)
    lcd_byte(0x01, LCD_CMD)
    gpio.cleanup()
    print("프로그램 종료")

