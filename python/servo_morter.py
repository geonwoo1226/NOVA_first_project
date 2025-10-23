import RPi.GPIO as gpio
import time

class ServoMorter:
    def __init__(self, roomNum):
        self.roomNum = roomNum
        
        if self.roomNum == 1:
            self.servo_pin = 16
        elif self.roomNum == 2:
            self.servo_pin = 13
        gpio.setmode(gpio.BCM)
        gpio.setup(self.servo_pin, gpio.OUT)
        
        self.pwm = gpio.PWM(self.servo_pin, 50)
    
    def curtain_open(self):
        try:
            self.pwm.start(2.5)
            time.sleep(0.5)
            for count in range(3):
                for i in range(30,126):
                    self.pwm.ChangeDutyCycle(i/10)
                    time.sleep(0.01)
                
                for i in range(125,29,-1):
                    self.pwm.ChangeDutyCycle(i/10)
                    time.sleep(0.001)
                time.sleep(0.3)
        finally:
            self.pwm.stop()
            gpio.cleanup()

ServoMorter(2).curtain_open()