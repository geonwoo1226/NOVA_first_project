import smbus2
import time

class LCD_Display:
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
    def lcd_run(self, message_1, message_2):
        try:
            self.lcd_string(message_1, self.LCD_LINE_1)
            self.lcd_string(message_2, self.LCD_LINE_2)
            time.sleep(5)
        finally:
            self.lcd_byte(0x01, self.LCD_CMD)
            self.bus.close()
    
    def warning_print(self, message):
        try:
            while True:
                self.lcd_string("Warning!!", self.LCD_LINE_1)
                self.lcd_string(message, self.LCD_LINE_2)
                time.sleep(1)
            
                self.lcd_byte(0x01, self.LCD_CMD)
                time.sleep(0.1)
        finally:
            self.lcd_byte(0x01, self.LCD_CMD)
            self.bus.close()