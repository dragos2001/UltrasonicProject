
#include <stdio.h>
#include "pico/stdlib.h"
// For ADC input:
#include "hardware/adc.h"
#include "hardware/dma.h"
// For resistor DAC output:
#include "pico/multicore.h"
#include "hardware/uart.h"
#include "pico/binary_info.h"
#include <inttypes.h>
#include <dma/dma.h>

int dma_capture_config( uint8_t capture_channel, size_t num_samples, float clock_div)  {

    stdio_init_all();
    adc_gpio_init(26 + capture_channel);
    adc_init();
    adc_select_input(capture_channel);
    adc_fifo_setup(true,true,1,true,false);
    adc_set_clkdiv(clock_div);
    sleep_ms(1000);

    //Set up DMA to start transferring data as soon as it appears in FIFO
    int dma_chan = dma_claim_unused_channel(true);
    dma_channel_config cfg = dma_channel_get_default_config(dma_chan);

     // Reading from constant address, writing to incrementing byte addresses
    channel_config_set_transfer_data_size(&cfg, DMA_SIZE_16);
    channel_config_set_read_increment(&cfg, false);
    channel_config_set_write_increment(&cfg, true);

    // Pace transfers based on availability of ADC samples
    channel_config_set_dreq(&cfg, DREQ_ADC);

    dma_channel_configure(
        dma_chan,
        &cfg,
        NULL, //array to store the data
        &adc_hw->fifo, //fifo
        num_samples, //num_samples
        false
          //start immediately
    );

    return dma_chan;   
  
}
uint64_t dma_capture_start(int dma_chan, uint16_t *buffer)
{

    // 1. Set writing address
    dma_channel_set_write_addr(dma_chan,buffer,true);
    // 2. Reset DMA channel for new transfer
    adc_fifo_drain();
    // 3. Start adc
    adc_run(true);

    printf("Starting capture\n");
    uint64_t start_time = get_absolute_time();

    // 5. Wait for DMA to finish
    dma_channel_wait_for_finish_blocking(dma_chan);

    // 6. Stop ADC (optional if you want to run continuously)
    adc_run(false);
    

    //End time
    uint64_t end_time = get_absolute_time();

    //Elapsed time
    uint64_t elapsed_time = end_time - start_time;

    printf("Elapsed time %llu\n", elapsed_time);
    printf("Finished capture\n");

    return elapsed_time;
}

uint64_t dma_capture_start_debug(int dma_chan, uint16_t *buffer, dma_channel_hw_t *hw )
{

    // 1. Set writing address
    dma_channel_set_write_addr(dma_chan,buffer,true);
    // 2. Reset DMA channel for new transfer
    adc_fifo_drain();
    // 3. Start adc
    adc_run(true);
    
    // 3. Start DMA
    //dma_channel_start(dma_chan);
    
    //printf("---After dma start---\n");
    //debug_dma(hw);
    // 4. Start ADC
   //adc_run(true);

    printf("Starting capture\n");
    uint64_t start_time = get_absolute_time();

    // 5. Wait for DMA to finish
    dma_channel_wait_for_finish_blocking(dma_chan);

    // 6. Stop ADC (optional if you want to run continuously)
    adc_run(false);
    

    //End time
    uint64_t end_time = get_absolute_time();

    //Elapsed time
    uint64_t elapsed_time = end_time - start_time;

    printf("Elapsed time %llu\n", elapsed_time);
    printf("Finished capture\n");

    return elapsed_time;
}

void debug_dma(dma_channel_hw_t *hw)
{  
    printf("Read address: 0x%08" PRIx32 "\n", hw -> read_addr);
    printf("Write address: 0x%08" PRIx32 "\n", hw -> write_addr);
    printf("Control and status: 0x%08" PRIx32 "\n", hw -> ctrl_trig);
    printf("Num of transfers: 0x%08" PRIx32 "\n", hw -> transfer_count);

}
