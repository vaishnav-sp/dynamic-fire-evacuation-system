import paho.mqtt.client as mqtt

from app.config.settings import MQTT_BROKER
from app.config.constants import MQTT_PORT


def create_client():

    return mqtt.Client()