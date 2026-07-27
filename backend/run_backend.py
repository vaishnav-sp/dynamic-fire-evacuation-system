import threading
import uvicorn

from app.main import app
from app.mqtt.subscriber import MQTTSubscriber



def start_mqtt():

    subscriber = MQTTSubscriber()

    subscriber.start()



if __name__ == "__main__":


    mqtt_thread = threading.Thread(
        target=start_mqtt,
        daemon=True
    )


    mqtt_thread.start()



    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )