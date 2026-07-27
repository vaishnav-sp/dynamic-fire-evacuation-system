def calculate_confidence(sensor_health, timestamp_valid):

    confidence = 1.0

    if sensor_health != "ONLINE":
        confidence -= 0.5

    if not timestamp_valid:
        confidence -= 0.3

    if confidence < 0:
        confidence = 0

    return confidence