/**
 * Copyright (c) 2021 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "hardware/gpio.h"
#include "hardware/adc.h"
#include "hardware/uart.h"
#include "hardware/clocks.h"
#include "pico/binary_info.h"
#include <inttypes.h>
#include "pico/stdlib.h"
#include <math.h>
#include <filter/filter.h>
#include <adc/adc.h>

/* Example code to extract analog values from a microphone using the ADC
   with accompanying Python file to plot these values

   Connections on Raspberry Pi Pico board, other boards may vary.

   GPIO 26/ADC0 (pin 31)-> AOUT or AUD on microphone board
   3.3v (pin 36) -> VCC on microphone board
   GND (pin 38)  -> GND on microphone board
*/

#define NUM_SAMPLES 1500
#define ADC_NUM 2
#define ADC_PIN 28 
#define ADC_VREF 3.3
#define ADC_RANGE (1 << 12)
#define ADC_CONVERT (ADC_VREF / (ADC_RANGE - 1))
#define USS_TRIG (10)
#define USS_ECHO (11)


uint64_t  full_adc_sending_pipeline( uint16_t *array, size_t num_samples)
{   
    send_receive_uss(USS_TRIG);
    uint64_t elapsed_time = sample_adc_data(array,num_samples);
    //send data
    send_data_serial_int(array,elapsed_time, num_samples);

    return elapsed_time;
}

int main() {

    stdio_init_all();
    bi_decl(bi_program_description("Analog daw data extraction for pico2")); // for picotool
    bi_decl(bi_1pin_with_name(ADC_PIN, "ADC input pin"));
    
    //initializations
    uss_init(USS_TRIG, USS_ECHO);
    adc_initialization(ADC_PIN, ADC_NUM,960);
    
    clock_configure(clk_adc,
                    0,
                    CLOCKS_CLK_ADC_CTRL_AUXSRC_VALUE_CLKSRC_PLL_USB,
                    48 * 1000 * 1000,
                    12 * 1050 * 1000);//you need to set the clock not the frequency 
                
        
    
    //array allocation
    uint16_t *array_samples = (uint16_t*)malloc(sizeof(uint16_t)*NUM_SAMPLES);

    //init 
    uint8_t meas_count = 1;
    char* const measure = "measure";
    char command[30];
    uint64_t processing_time;

    while(1) 
    {
        // Read command
        scanf("%s",command);
        if (strcmp(command,measure) == 0)  {
            //printf("Sys clock: %"PRIu32"\n",sys_hz);
            //Start Measurement
            printf("Start Measurement %hhu\n", meas_count);  
            //Full adc processing
            processing_time = full_adc_sending_pipeline(array_samples,NUM_SAMPLES);
            sleep_ms(1);
            //Elapsed time
            printf("Elapsed time: %llu\n", processing_time);
            sleep_ms(1);
            //Sampling freq
            printf("Sampling Frequency: %.3f kHz\n", ((float)NUM_SAMPLES / processing_time) * 1000);
            sleep_ms(1);
            //End directive
            printf("End Measurement %hhu\n", meas_count);
        }
        meas_count++;
    }
}
