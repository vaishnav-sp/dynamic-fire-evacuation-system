#ifndef MQTT_HANDLER_H
#define MQTT_HANDLER_H


#include <Arduino.h>


void mqtt_setup();

void mqtt_loop();

void publish_sensor_data(
    float temperature,
    float smoke,
    bool flame,
    int occupancy
);


#endif