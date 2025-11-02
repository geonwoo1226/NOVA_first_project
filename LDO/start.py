import project_mqtt
import time

# 메인 시작 부분
if __name__ == "__main__":
    try:
        mqtt = project_mqtt.MqttWorker()
        mqtt.mqtt_connect()
        
    except KeyboardInterrupt:
        pass
    finally:
        print("종료")