import project_mqtt
import time


if __name__ == "__main__":
   
    try:
        mqtt = project_mqtt.MqttWorker()
        mqtt.mqtt_connect()
        
            
    except KeyboardInterrupt as error:
        print(error)
    finally:
        print("종료")