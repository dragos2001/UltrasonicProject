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
#include "pico/binary_info.h"
#include <inttypes.h>
#include "pico/stdlib.h"
#include <math.h>

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

void adc_initialization()
{
    //configure adc
    adc_init();
    adc_gpio_init( ADC_PIN);
    adc_select_input( ADC_NUM);

}
void uss_init()
{

    //configure ultrasonic sensor
    gpio_init(USS_TRIG);
    gpio_init(USS_ECHO);

    //set direction
    gpio_set_dir(USS_TRIG,GPIO_OUT);
    gpio_set_dir(USS_ECHO,GPIO_IN);
    gpio_pull_down(USS_TRIG);
    gpio_pull_up(USS_ECHO);

}
void trigger_uss(bool state)
{

    gpio_put(USS_TRIG,state);

}
void send_receive_uss()
{   
    trigger_uss(1);
    sleep_us(20);
    trigger_uss(0);
}
uint64_t sample_adc_data(uint16_t* data)
{   
    absolute_time_t start_time = get_absolute_time();
    for (uint16_t i = 0; i < NUM_SAMPLES; i++)
        data[i]  = adc_read();
    absolute_time_t end_time = get_absolute_time();

    uint64_t elapsed_time = absolute_time_diff_us(start_time,end_time);
    
    return elapsed_time; 
}
void send_data_serial(uint16_t *array, uint64_t sample_time)
{   
    uint16_t i;
    uint64_t time_step;
    for (i = 0; i<NUM_SAMPLES; i++)
        {   
           
            time_step  = i * sample_time;
            printf("%llu,%hu\n", time_step, array[i]);
            sleep_ms(1);
       }
}
uint64_t  full_adc_sending_pipeline( uint16_t *array)
{   
    send_receive_uss();
    uint64_t elapsed_time = sample_adc_data(array);//!s
    //compute 
    uint64_t sample_time = elapsed_time / NUM_SAMPLES;
    //send data
    send_data_serial(array,sample_time);

    return elapsed_time;
}

int main() {

    stdio_init_all();
    bi_decl(bi_program_description("Analog daw data extraction for pico2")); // for picotool
    bi_decl(bi_1pin_with_name(ADC_PIN, "ADC input pin"));
    
    //initializations
    uss_init();
    adc_initialization();
    
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
            //Start Measurement
            printf("Start Measurement %hhu\n", meas_count);
            //Full adc processing
            processing_time = full_adc_sending_pipeline(array_samples);
            //Elapsed time
            printf("Elapsed time: %llu\n", processing_time);
            //End directive
            printf("End Measurement %hhu\n", meas_count);
        }
        meas_count++;
    }
}
