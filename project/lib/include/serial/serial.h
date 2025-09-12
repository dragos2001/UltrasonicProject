#ifndef SERIALLIB_H
#define SERIALLIB_H
#include <stdint.h>
void send_data_serial_float( size_t num_samples , float array[num_samples], float sample_time);
void send_data_serial_int( size_t num_samples , uint16_t array[num_samples], float sample_time);

#endif