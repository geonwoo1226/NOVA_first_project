# 일단 보류
from mfrc522 import SimpleMFRC522
import time

class RFID:
    def __init__(self):
        self.reader = SimpleMFRC522()
        
    def RFID_id(self, id):
        return id
    
    # 
    def RFID_on(self):
        try:
            print("===================================")
            print(" RFID 태그를 리더기에 대주세요...")
            print("===================================")
            while True:
                id, text = self.reader.read()
                print(f"\n[RFID가 감지되었습니다.]")
                print(f"카드 ID : {id}")
                print("-----------------------------------")
                time.sleep(1)
                break
        except KeyboardInterrupt:
            pass
        finally:
            self.RFID_id(id)