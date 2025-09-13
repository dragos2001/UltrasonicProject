#ifndef FFTLIB_H
#define FFTLIB_H

#include <stdint.h>   // for uint8_t, uint16_t, uint64_t
#include <stddef.h>   // for size_t
#include <stdbool.h>  // for bool
#include <complex.h>

void fft_n(int n, float complex *samples , float complex *temp);
void ifft_n(int n, float complex *fft_samples, float complex *temp);
int get_fft_size(int n);
void compute_analytic_signal(int n, float complex *analytic_signal, float complex *temp);
void compute_envelope(int n, float *envelope,  float complex *analytic_signal);
void padd_signal(int n, float complex *padded_signal,float *input_samples );


#endif