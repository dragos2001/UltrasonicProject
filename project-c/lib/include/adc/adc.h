#ifndef ADCLIB_H
#define ADCLIB_H

#include <stdint.h>   // for uint8_t, uint16_t, uint64_t
#include <stddef.h>   // for size_t
#include <stdbool.h>  // for bool

void adc_initialization( uint8_t adc_pin, uint8_t adc_num);
void uss_init(uint8_t uss_trig, uint8_t uss_echo);
void trigger_uss(uint8_t uss_trig, bool state);
void send_receive_uss(uint8_t uss_trig);
uint64_t sample_adc_data(uint16_t data[], size_t num_samples);
void send_data_serial(uint16_t array[], uint64_t sample_time, size_t num_samples);

#endif