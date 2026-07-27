#include "mqtt_handler.h"
#include "config.h"

#include <WiFi.h>
#include <PubSubClient.h>


WiFiClient espClient;

PubSubClient mqttClient(espClient);



void reconnect()
{

    while(!mqttClient.connected())
    {

        Serial.println("Connecting MQTT...");


        if(mqttClient.connect(NODE_ID))
        {

            Serial.println("MQTT Connected");

        }

        else
{

            Serial.print("MQTT failed, rc=");
            Serial.println(mqttClient.state());

            delay(2000);

        }

    }

}




void mqtt_setup()
{

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );


    Serial.print("Connecting WiFi");


    while(WiFi.status()!=WL_CONNECTED)
    {

        delay(500);

        Serial.print(".");

    }


    Serial.println();

    Serial.println("WiFi Connected");


    mqttClient.setServer(
        MQTT_SERVER,
        MQTT_PORT
    );


}




void mqtt_loop()
{

    if(!mqttClient.connected())
    {
        reconnect();
    }


    mqttClient.loop();

}





void publish_sensor_data(
    float temperature,
    float smoke,
    bool flame,
    int occupancy
)
{

    String topic =
        "building/node/" NODE_ID;


    String payload =
        "{";

    payload += "\"node_id\":\"";
    payload += NODE_ID;
    payload += "\",";


    payload += "\"node_type\":\"ESP32\",";


    payload += "\"temperature\":";
    payload += temperature;
    payload += ",";


    payload += "\"smoke\":";
    payload += smoke;
    payload += ",";


    payload += "\"flame\":";
    payload += flame ? "true":"false";
    payload += ",";


    payload += "\"occupancy\":";
    payload += occupancy;


    payload += "}";


    mqttClient.publish(
        topic.c_str(),
        payload.c_str()
    );


    Serial.println(payload);

}