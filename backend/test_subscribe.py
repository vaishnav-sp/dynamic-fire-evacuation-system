from app.mqtt.subscriber import Subscriber

subscriber = Subscriber()

subscriber.connect()

subscriber.start()