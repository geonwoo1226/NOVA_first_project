import project_mqtt
import time

if __name__ == "__main__":
    try:
        mqtt = project_mqtt.MqttWorker()
        mqtt.mqtt_connect()
        
            
    except KeyboardInterrupt:
        pass
    finally:
        print("종료")   