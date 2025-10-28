import RPi.GPIO as gpio
import board
import adafruit_dht
from first_project.led_sensor import LED
from first_project.buzzer import Buzzer
from threading import Thread

# 핀번호 고정부여 / 온습도값 부여
mydht11 = adafruit_dht.DHT11(board.D26)
humidity_data = mydht11.humidity
temperature_data = mydht11.temperature

buzzer = Buzzer()
led = LED()

led_switch = Thread(target=led.led_switch)
kitchen_buzzer = Thread(target=buzzer.kitchen_buzzer)

led_switch.start()
kitchen_buzzer.start()
try:
    print("화재발생")
    led_switch.join()
    kitchen_buzzer.join()
finally:
    print("화재경보 중지")
    buzzer.stop_buzzer()