# -*- coding: utf-8 -*-
"""
Created on Sun Aug 31 18:49:32 2025

@author: BRD5CLJ
"""

from butterworth import  MultiBiquadFloat
from scipy.signal import hilbert
from utils import FileHandler
import pandas as pd
import numpy as np
from discrete_hilbert import FILTER_COEFFS,compute_hilbert,compute_envelope
from plot.plot_signal import plot_signal
import time
if __name__ == "__main__":

    fh = FileHandler()
    path = fh.select_file()
    butterworth_filter = MultiBiquadFloat()
    
    #read data
    data_frame = pd.read_csv(path)
    signal = data_frame.iloc[:,1]
    timestamps = data_frame.iloc[:,0]
    
    #signal
    filtered_signal = np.array(butterworth_filter.apply_filter(signal))
    plot_signal(timestamps,filtered_signal,title="Filtered Butterworth")
    
    #hilbert - scipy
    start = time.time()
    envelope_scipy = np.abs(hilbert(filtered_signal))
    # End timer
    end = time.time()
    elapsed_time_hilbert_original = end - start
    
    plot_signal(timestamps,envelope_scipy,title="Envelope Scipy")
    
    
    #hilbert - convolution manual made
    filtered_padded = np.pad(filtered_signal,(0,30))
    start = time.time()
    hilbert_transform=[]
    buffer = np.zeros(31)
    for i in range (len(filtered_padded)):
         buffer[ (30+i) % 31] = filtered_padded[i]
         y=0
         for j in range (31):
             y +=  FILTER_COEFFS[j] * buffer[(30+i-j)%31]
         hilbert_transform.append(y)
    end =time.time()    
    #plot the hilbert transform
    extracted_hilbert = np.array(hilbert_transform[15:-15])
    plot_signal(timestamps,extracted_hilbert,"Hilbert transform")
    envelope_convolve = np.abs(extracted_hilbert * i + filtered_signal)
    
    elapsed_time_hilbert2 = end-start 
    plot_signal(timestamps,envelope_convolve,"Envelope convolve manual")
    
    
    
    #hilbert - numpy
    start=time.time()
    hilbert_numpy = compute_hilbert(filtered_signal,FILTER_COEFFS)
    envelope_convolve_numpy = compute_envelope(filtered_signal,hilbert_numpy[15:-15])
    end=time.time()
    elapsed_time_hilbert3=end-start
    plot_signal(timestamps,hilbert_numpy[15:-15],"Hilbert convolve numpy")
    plot_signal(timestamps,envelope_convolve_numpy,"Emvelope Hilbert numpy")
         
   
    

             