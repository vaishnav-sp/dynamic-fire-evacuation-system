from app.hazard.sensor_fusion import SensorFusion


fusion = SensorFusion()


normal = {

    "temperature":25,
    "smoke":0,
    "flame":0,
    "occupancy":10

}


fire = {

    "temperature":150,
    "smoke":80,
    "flame":90,
    "occupancy":20

}


print(
    "Normal Hazard:",
    fusion.calculate(normal)
)


print(
    "Fire Hazard:",
    fusion.calculate(fire)
)