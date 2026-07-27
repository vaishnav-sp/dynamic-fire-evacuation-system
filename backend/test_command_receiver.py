import paho.mqtt.client as mqtt


def on_message(client, userdata, msg):

    print(
        msg.topic,
        msg.payload.decode()
    )



client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)


client.on_message = on_message


client.connect(
    "localhost",
    1883
)


client.subscribe(
    "building/command/#"
)


client.loop_forever()