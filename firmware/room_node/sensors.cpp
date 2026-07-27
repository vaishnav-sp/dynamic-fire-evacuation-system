#include "sensors.h"

#include <Arduino.h>
#include <DHT.h>


#define DHT_PIN 16
#define DHT_TYPE DHT11


#define MQ2_PIN 34


#define FLAME_PIN 27


#define PIR_PIN 25



DHT dht(
    DHT_PIN,
    DHT_TYPE
);



void sensors_setup()
{

    dht.begin();


    pinMode(
        FLAME_PIN,
        INPUT
    );


    pinMode(
        PIR_PIN,
        INPUT
    );

}




float read_temperature()
{

    float t = dht.readTemperature();


    Serial.print("DHT RAW: ");
    Serial.println(t);


    return t;

}




float read_smoke()
{

    int value = analogRead(
        MQ2_PIN
    );


    return map(
        value,
        0,
        4095,
        0,
        100
    );

}




bool read_flame()
{

    int value = digitalRead(FLAME_PIN);


    return value == LOW;

}




int read_occupancy()
{

    return digitalRead(
        PIR_PIN
    );

}