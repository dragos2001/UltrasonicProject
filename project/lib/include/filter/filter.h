#ifndef FILTLIB_H
#define FILTLIB_H

#include <stdint.h>   // for uint8_t, uint16_t, uint64_t

extern const double BIQUAD_LAYERS_CASCADE_5[5][5];
double apply_biquad( double input_sample, const double *filter_coefs, double *hidden_state, uint8_t index);
int16_t saturate_q15(double x);
double normalize_q15(int x);
double filter_butterworth_biquad_online(uint8_t rows, uint16_t x, const double filter_matrix[rows][5], double *hidden_state);
void filter_butterworth_biquad_postprocessing(uint8_t rows, uint16_t * input_data, float*output_data, const double filter_matrix[rows][5], double *hidden_states, size_t num_samples);

#endif