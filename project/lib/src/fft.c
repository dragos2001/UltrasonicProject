#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>
#include "pico/binary_info.h"
#include <inttypes.h>
#include "pico/stdlib.h"

void fft_n(int n, float complex *samples , float complex *temp)
{

    if (n == 1)
        {
            return;
        }

    for (int i = 0 ; i< n/2 ; i++)
    { 
            temp[i] = samples[2*i] ;
            temp[i + n/2] = samples[2*i + 1] ;
    }
   
    fft_n(n/2 , temp, samples);
    fft_n(n/2 , temp + n/2, samples + n/2);
    
    float complex  w = cos(2 * M_PI/n) - I *sin(2 * M_PI/n);
    float complex w_i = 1;

    for (int i=0 ; i<n/2 ; i++)
    {   
        samples[i] = temp[i] + w_i * temp[i + n/2];
        samples[i+n/2] = temp[i] - w_i * temp[i + n/2];
        w_i = w_i * w;
    }

    
}
void ifft_n(int n, float complex *fft_samples, float complex *temp)
{

    if (n == 1)
    {

        return;

    }
    
    for (int i=0 ; i < n/2; i++)
    { 
        temp[i] = fft_samples[2*i];
        temp[i+n/2] = fft_samples[2 * i + 1];
    }

    
    ifft_n(n/2 , temp, fft_samples);
    ifft_n(n/2 , temp + n/2, fft_samples + n/2);

    float complex  w = cos(2 * M_PI / n) + I*sin(2 * M_PI / n);
    float complex w_i = 1;

    for (int i = 0; i < n/2; i++)
    {       
        fft_samples[i] = temp[i] + w_i* temp[i + n/2];
        fft_samples[i+n/2] = temp[i] - w_i * temp[i + n/2];
        w_i=w_i*w;
    }
}

int get_fft_size(int n)
{
    int fft_length;
    if ((n>0) && ((n & (n-1)) ==0))
    {
            fft_length = n;
    }    
    else 
    {         
            fft_length = 1<< (int)ceil(log2f(n));
    }
    return fft_length;
}

void padd_signal(int n , float complex *padded_signal, float *input_samples)
{
   
    for (int i = 0; i<n ;i++)
    {
        padded_signal[i] = input_samples[i];
    }
}

void compute_analytic_signal(int n, float complex *analytic_signal, float complex *temp )
{
    fft_n(n,analytic_signal,temp);
    for (int i = 1; i<= n / 2; i++)
    {
        analytic_signal[i] = 2 * analytic_signal[i];
    }
    for (int i = n/ 2 + 1 ; i < n; i++)
    {
        analytic_signal[i] = 0;
    }
    ifft_n(n, analytic_signal, temp);
    
    //normalize
    for (int i =0; i< n; i++)
    {
        analytic_signal[i]= analytic_signal[i]/ n;
    }

}

void compute_envelope(int n, float *envelope,float complex *analytic_signal)
{
    for (int i = 0; i< n ; i++)
    {
        envelope[i] = sqrt( creal(analytic_signal[i]) * creal(analytic_signal[i]) + cimag(analytic_signal[i]) * cimag(analytic_signal[i]) );
    }

}




