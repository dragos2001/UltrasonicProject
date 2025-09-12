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
#include "hardware/pio.h"
#include "hardware/dma.h"
#include "pico/binary_info.h"
#include <inttypes.h>
#include "pico/stdlib.h"
#include <math.h>
#include <filter/filter.h>
#include <adc/adc.h>
#include <dma/dma.h>
#include <serial/serial.h>

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
    bi_decl(bi_program_description("Capture dma analog samples")); // for picotool
    bi_decl(bi_1pin_with_name(ADC_PIN, "ADC input pin"));
    
    //uss initializations
    uss_init(USS_TRIG, USS_ECHO);
    
    /*clock_configure(clk_adc,
                    0,
                    CLOCKS_CLK_ADC_CTRL_AUXSRC_VALUE_CLKSRC_PLL_USB,
                    48 * 1000 * 1000,
                    12 * 1000 * 1000);//you need to set the clock not the frequency 
    */

    //array allocation
    uint16_t array_samples[NUM_SAMPLES];
    //dma configure
    int dma_chan = dma_capture_config(array_samples, ADC_NUM, NUM_SAMPLES, 394);//achive micropython sampling rate
    dma_channel_hw_t *hw = dma_channel_hw_addr(dma_chan);
    //sampling times
    uint64_t elapsed_time;
    uint32_t freq_adc;
    //init 
    uint8_t meas_count = 1;
    char* const measure = "measure";
    char command[30];
    while(1)
    {
        // Read command
        scanf("%s",command);
        if (strcmp(command,measure)==0)
        { 
          //debug_dma(hw);
          printf("Start measurement\n");
          freq_adc = clock_get_hz(clk_adc);
          printf("Clock frequency is %" PRIu32 "\n",freq_adc);
          sleep_ms(1);
          send_receive_uss(USS_TRIG);
          elapsed_time = dma_capture_start(dma_chan, array_samples, hw);
          send_data_serial_int(array_samples,elapsed_time,NUM_SAMPLES);
          printf("Smpling time: %f \n", (float)elapsed_time/NUM_SAMPLES);
          printf("End measurement\n");
          
        }
    }
    dma_channel_unclaim(dma_chan);
   
}
