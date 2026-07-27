import json
import paho.mqtt.client as mqtt



class ActuatorPublisher:


    def __init__(self):

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        self.client.connect(
            "localhost",
            1883
        )



    def send_command(
        self,
        node_id,
        led_state,
        pattern="NORMAL"
    ):


        payload = {

            "node_id": node_id,

            "led": led_state,

            "pattern": pattern

        }


        topic = (
            f"building/command/{node_id}"
        )


        self.client.publish(

            topic,

            json.dumps(payload)

        )


        print(
            "ACTUATOR COMMAND:",
            payload
        )