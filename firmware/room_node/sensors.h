#ifndef SENSORS_H
#define SENSORS_H


void sensors_setup();


float read_temperature();


float read_smoke();


bool read_flame();


int read_occupancy();


#endif