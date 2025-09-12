#include <inttypes.h>
#include "pico/stdlib.h"
#include <stdio.h>


void send_data_serial_int( size_t num_samples , uint16_t array[num_samples], float sample_time)
{   
 
    for (size_t i = 0; i< num_samples; i++)
        {              
            printf("%.6f, %d\n", sample_time*i, array[i]);
            sleep_ms(1);
       }
}

void send_data_serial_float(size_t num_samples, float array[], float sample_time)
{   
 
    for (size_t i = 0; i< num_samples; i++)
        {              
            printf("%.6f , %f\n", sample_time*i, array[i]);
            sleep_ms(1);
        }
}



