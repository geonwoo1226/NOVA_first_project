#push_switch_polling_test.py
#푸시버튼을 이용하는 방법은 폴링과 인터럽트방식이 있다.
#폴링은 간단하게 구현 가능
#프로그램이 무한 루프를 실행하면서 버튼이 눌려지는 것을 끊임없이 확인
import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
pin = 12
gpio.setup(pin,gpio.IN, pull_up_down=gpio.PUD_UP)
while 1:
    input_val = gpio.input(pin)
    print(input_val)
    if input_val == gpio.LOW:
        print("버튼이 눌려짐")
        break
    time.sleep(0.5)
    
gpio.cleanup()
