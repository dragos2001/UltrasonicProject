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
#include <serial/serial.h>
#include <float.h>
#include <dma/dma.h>
#include <fft/fft.h>

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



int main() {

    stdio_init_all();
    bi_decl(bi_program_description("Analog daw data extraction for pico2")); // for picotool
    bi_decl(bi_1pin_with_name(ADC_PIN, "ADC input pin"));

    //array allocation
    uint16_t adc_samples[NUM_SAMPLES];
    float filtered_samples[NUM_SAMPLES];
    double *hidden_states = (double*)malloc(10*(sizeof(double)));

    //envelope allocation
    int fft_length = get_fft_size(NUM_SAMPLES);  
    float complex analytic_signal[fft_length];
    float complex temp[fft_length];
    float envelope[fft_length];
    float sampling_rate;
    //initializations
    uss_init(USS_TRIG, USS_ECHO);
    int dma_chan = dma_capture_config(ADC_NUM, NUM_SAMPLES, 394);
    //metadata 
    uint8_t meas_counter = 1;
    char* const measure = "measure";
    char command[30];
    uint64_t processing_time;
    uint64_t start_time;
    uint64_t end_time;
    while(1) 
    {
        // Read command
        scanf("%s",command);
        if (strcmp(command,measure) == 0)  
        {
        
            //Start Measurement
            printf("Start Measurement %hhu\n", meas_counter);  
            //Full adc processing
            send_receive_uss(USS_TRIG);
            processing_time = dma_capture_start( dma_chan,adc_samples);
            sampling_rate = (float)processing_time / NUM_SAMPLES;

            //Start counting
            start_time = get_absolute_time();
            //Filter data
            memset(hidden_states,0,10*sizeof(double));
            filter_butterworth_biquad_postprocessing(5, adc_samples, filtered_samples, BIQUAD_LAYERS_CASCADE_5, hidden_states,  NUM_SAMPLES);
            //Envelope
            padd_signal(NUM_SAMPLES, analytic_signal, filtered_samples);
            compute_analytic_signal(fft_length, analytic_signal,filtered_samples);
            compute_envelope(fft_length, envelope,  analytic_signal);
            //Stop counting
            end_time = get_absolute_time();
            
            //Send data serial
            send_data_serial_float(NUM_SAMPLES, filtered_samples, sampling_rate);
            send_data_serial_float(NUM_SAMPLES, envelope, sampling_rate);
            
            //Sampling freq
            printf("Sampling Frequency: %.3f kHz\n", 1 / sampling_rate * 1000);
            //Elapsed time
            printf("Elapsed dma time: %llu\n", processing_time);
            printf("Elapsed processing time: %llu\n", end_time-start_time);
            //End directive
            printf("End Measurement %hhu\n", meas_counter);
        }
        meas_counter++;
        
    }
    free(hidden_states);
}
