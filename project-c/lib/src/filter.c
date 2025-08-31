#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "hardware/gpio.h"
#include "hardware/adc.h"
#include "hardware/uart.h"
#include "pico/binary_info.h"
#include <inttypes.h>
#include "pico/stdlib.h"


const float BIQUAD_LAYERS[5][5] = {{5.49496377e-04, -1.09899275e-03,  5.49496377e-04 , 7.75752801e-01,  5.82317689e-01},
                                {1.00000000e+00, -2.00000000e+00,  1.00000000e+00, 5.54213901e-01,  6.30454831e-01},
                                {1.00000000e+00,  0.00000000e+00, -1.00000000e+00, 1.03575406e+00,  6.80934131e-01},
                                {1.00000000e+00,  2.00000000e+00,  1.00000000e+00, 4.52443546e-01,  8.39682131e-01},
                                {1.00000000e+00,  2.00000000e+00,  1.00000000e+00, 1.26801640e+00,  8.75731512e-01},
                                };

float apply_biquad( float input_sample, float *filter_coefs, float*hidden_state)  {
    //declare output
    float output_sample;
    //compute output
    output_sample = filter_coefs[0] * input_sample + hidden_state[0];
    //update hidden states
    hidden_state[0]= filter_coefs[1] * input_sample - filter_coefs[3] * output_sample + hidden_state[1];
    hidden_state[1] = filter_coefs[2] * input_sample - filter_coefs[4] * output_sample;
    return output_sample;
}

int16_t saturate_q15(float x)
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

 static float normalize_q15(int x)
{   
    float y = (float)(x + 32768.0f)/(32767 + 32768);

    return y;
}

//filter data
int16_t filter_butterworth_biquad_online(uint16_t x, float **filter_matrix, float *hidden_state)  {

    float y = x;
    for (int j = 0; j < 5; j++)
        {       
            y = apply_biquad( y, *(filter_matrix + j ), (hidden_state + 2*j ));
        }
    return saturate_q15(y); 
}


void filter_butterworth_biquad_postprocessing(uint16_t * input_data, int16_t *output_data, float filter_matrix[5][5], float *hidden_states, uint16_t num_samples)  {
 
    for (uint16_t i = 0; i <  num_samples; i++)
    {   
        float out_sample = (float)input_data[i];
        for (uint8_t j = 0; j < 5; j++)
        {       
            out_sample= apply_biquad(out_sample, *(filter_matrix + j), (hidden_states + 2*j));
        }
        output_data[i] = saturate_q15(out_sample);
    }
}

