#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "hardware/gpio.h"
#include "hardware/adc.h"
#include "hardware/uart.h"
#include "pico/binary_info.h"
#include <inttypes.h>
#include "pico/stdlib.h"
#include <filter/filter.h>



const double BIQUAD_LAYERS_CASCADE_5[5][5] = {{5.49496377e-04, -1.09899275e-03,  5.49496377e-04 , 7.75752801e-01,  5.82317689e-01},
                                {1.00000000e+00, -2.00000000e+00,  1.00000000e+00, 5.54213901e-01,  6.30454831e-01},
                                {1.00000000e+00,  0.00000000e+00, -1.00000000e+00, 1.03575406e+00,  6.80934131e-01},
                                {1.00000000e+00,  2.00000000e+00,  1.00000000e+00, 4.52443546e-01,  8.39682131e-01},
                                {1.00000000e+00,  2.00000000e+00,  1.00000000e+00, 1.26801640e+00,  8.75731512e-01},
                                };
                                
double apply_biquad( double input_sample, const double *filter_coefs, double *hidden_state, uint8_t index)  {
    
    //declare output
    double output_sample;
    //compute output
    output_sample = filter_coefs[0] * input_sample + hidden_state[index];
    //update hidden states
    hidden_state[index] = filter_coefs[1] * input_sample - filter_coefs[3] * output_sample + hidden_state[index+1];
    hidden_state[index+1] = filter_coefs[2] * input_sample - filter_coefs[4] * output_sample;
    return output_sample;
    
}

int16_t saturate_q15(double x)
{
    if (x < -(1<<15))
    {
        x = -(1<<15);
    }
    else if (x > (1<<15) - 1)
    {
        x = (1<<15) - 1;
    }
    return (int16_t)x;
}

double normalize_q11(int x)
{   
    double y = (double)(x + 2048.0) / (2047.0 + 2048.0);

    return y;
}

//filter data
double filter_butterworth_biquad_online(uint8_t rows, uint16_t x, const double filter_matrix[rows][5],double *hidden_state)  {

    double y = (x - 2048.0f) / 2048.0f;
    for (uint8_t j = 0 ; j < rows ; j++)
        {       
            y = apply_biquad(y, filter_matrix[j], hidden_state , 2*j);
        }
    return y;
}


void filter_butterworth_biquad_postprocessing(uint8_t rows, uint16_t * input_data, float *output_data, const double filter_matrix[rows][5], double *hidden_states, size_t num_samples)  {
 
    for (size_t i = 0 ; i <  num_samples ; i++)
    {   
        double out_sample = (input_data[i] - 2048.0) / 2048.0;
        for (uint8_t j = 0; j < rows; j++)
        {       
            out_sample = apply_biquad(out_sample, filter_matrix[j], hidden_states, 2*j);
        }
        output_data[i] = (float)out_sample;
    }
}

