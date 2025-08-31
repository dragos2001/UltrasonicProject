# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 22:39:51 2025

@author: BRD5CLJ
"""
from utils import FileHandler
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

def compute_hilbert(input_data, fir_filter):
    y = np.convolve(input_data,fir_filter,'full')
    return y
      
def compute_envelope(input1,input2):
  envelope=[]
  for i in range(1000):
      envelope.append(math.sqrt(input1[i]**2 + input2[i]**2))    
  return envelope
FILTER_COEFFS = [-0.0033953055, 0.0000000000, -0.0058651823, 0.0000000000, -0.0134384601, 0.0000000000, -0.0281422851, 0.0000000000,
 -0.0534836178, 0.0000000000, -0.0980394449, 0.0000000000, -0.1935637786, 0.0000000000, -0.6302204044, 0.0000000000,
  0.6302204044, 0.0000000000,  0.1935637786, 0.0000000000,  0.0980394449, 0.0000000000,  0.0534836178, 0.0000000000,
  0.0281422851, 0.0000000000,  0.0134384601, 0.0000000000,  0.0058651823, 0.0000000000,  0.0033953055]        
    
if __name__ =="__main__":
    
    

    fh = FileHandler()
    path = fh.select_file()
    data_frame = pd.read_csv(path)
    input_signal = data_frame["filtered_signal"]
    plt.plot(data_frame["Timestamps"], input_signal)
    plt.show()
    hilbert_signal = compute_hilbert(input_signal,FILTER_COEFFS )
    hilbert_non_delayed=hilbert_signal[15:-15]
    plt.plot(data_frame["Timestamps"] ,hilbert_non_delayed)
    plt.show()
    analytical_signal=[]
    envelope=[]
    for i in range(1000):
        envelope.append(math.sqrt(hilbert_non_delayed[i]**2 + input_signal[i]**2))
    plt.plot(input_signal)
    plt.plot(envelope)
    plt.show()