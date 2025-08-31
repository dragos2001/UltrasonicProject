#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "hardware/gpio.h"
#include "hardware/adc.h"
#include "hardware/uart.h"
#include "pico/binary_info.h"
#include <inttypes.h>
#include "pico/stdlib.h"


void adc_initialization( uint8_t adc_pin, uint8_t adc_num)
{
    //configure adc
    adc_init();
    adc_gpio_init( adc_pin);
    adc_select_input( adc_num);

}
void uss_init(uint8_t uss_trig, uint8_t uss_echo)
{

    //configure ultrasonic sensor
    gpio_init(uss_trig);
    gpio_init(uss_echo);

    //set direction
    gpio_set_dir(uss_trig,1);
    gpio_set_dir(uss_echo,0);
    gpio_pull_down(uss_trig);
    gpio_pull_up(uss_echo);

}
void trigger_uss(uint8_t uss_trig, bool state)
{

    gpio_put(uss_trig,state);

}
void send_receive_uss(uint8_t uss_trig)
{   
    trigger_uss(uss_trig,1);
    sleep_us(20);
    trigger_uss(uss_trig,0);
}
uint64_t sample_adc_data(uint16_t data[], size_t num_samples)
{   
    absolute_time_t start_time = get_absolute_time();
    for (uint16_t i = 0; i < num_samples; i++)
        data[i]  = adc_read();
    absolute_time_t end_time = get_absolute_time();

    uint64_t elapsed_time = absolute_time_diff_us(start_time,end_time);
    
    return elapsed_time; 
}
void send_data_serial(uint16_t array[], uint64_t sample_time, size_t num_samples)
{   
    uint16_t i;
    uint64_t time_step;
    for (i = 0; i< num_samples;i++)
        {              
            time_step  = i * sample_time;
            printf("%llu,%hu\n", time_step, array[i]);
            sleep_ms(1);
       }
}
uint64_t full_adc_sending_pipeline( uint16_t array[], size_t num_samples, uint8_t uss_trig)
{   
    send_receive_uss(uss_trig);
    uint64_t elapsed_time = sample_adc_data(array,num_samples);//!s
    //compute 
    uint64_t sample_time = elapsed_time / num_samples;
    //send data
    send_data_serial(array,sample_time,num_samples);

    return elapsed_time;
}