from app.mqtt.actuator_publisher import ActuatorPublisher


publisher = ActuatorPublisher()


publisher.send_command(
    "R2",
    "ON",
    "CRITICAL"
)