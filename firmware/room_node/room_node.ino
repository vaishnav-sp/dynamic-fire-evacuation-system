#include "mqtt_handler.h"
#include "sensors.h"


unsigned long lastPublish = 0;



void setup()
{

    Serial.begin(115200);


    sensors_setup();


    mqtt_setup();

}



void loop()
{

    mqtt_loop();



    if(
        millis()-lastPublish > 2000
    )
    {

        lastPublish = millis();



        float temperature =
            read_temperature();


        float smoke =
            read_smoke();


        bool flame =
            read_flame();


        int occupancy =
            read_occupancy();



        publish_sensor_data(

            temperature,

            smoke,

            flame,

            occupancy

        );


    }

}