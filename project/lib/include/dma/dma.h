#ifndef DMALIB_H
#define DMALIB_H
#include<stdint.h>
#include "hardware/dma.h"

int dma_capture_config(uint8_t capture_channel, size_t num_samples, float clk_div);
uint64_t dma_capture_start_debug(int dma_chan, uint16_t *buffer, dma_channel_hw_t *hw );
void debug_dma(dma_channel_hw_t *hw );
uint64_t dma_capture_start(int dma_chan, uint16_t *buffer);

#endif