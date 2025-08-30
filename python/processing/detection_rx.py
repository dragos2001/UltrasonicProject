# -*- coding: utf-8 -*-
"""
Created on Sun Jun 29 16:00:17 2025

@author: BRD5CLJ
"""
import matplotlib.pyplot as plt
import pandas as pd
import csv
import numpy as np
from scipy.signal import correlate
from math import ceil
from scipy.signal import hilbert
from scipy.signal import butter,sosfilt,filtfilt
from view_analog_signal import get_data
from utils import FileHandler
import sys
def get_index_start(timestamps):
    
    i=0
    while True:
       if timestamps[i] < 0:
           i=i+1
       else:
           break
    
    return i

def detect_by_hilbert_anvelope_pipeline( signal , timestamps , period , fs , min_time = 0.0015, threshold=0.25):
    start_idx = get_index_start(timestamps)
    len_tx = int(period * fs) 
    min_idx = start_idx + int(min_time * fs)
    sa=hilbert(signal)
    anvelope = np.abs(sa)
    phase=np.angle(sa)
    max_a = max(signal)
    ok = False
    for idx in range(0,len(anvelope)):   
                if idx > min_idx:                   
                    if anvelope[idx] >= max_a * threshold:
                        if ok==False:
                            start_idx = idx
                            ok=True
                    elif ok == True:
                        end_idx = idx    
                        break
                    
    return start_idx,end_idx,anvelope,phase
            
def detect_by_rectified_anvelope_pipeline( signal , timestamps , period , fs , min_time = 0.0015, threshold=0.25):
    start_idx = get_index_start(timestamps)
    len_tx = int(period * fs) 
    min_idx = start_idx + int(min_time * fs)
    rx_timestamp_idxs = np.array([],dtype=int)
    max_a = max(signal)
    ok = False
    y=0
    alfa=0.05
    t = threshold * max_a
    #anvelope
    anvelope=[]
    ok=False
    tracking=True
    for idx in range(0,len(signal)):   
                y = (1-alfa)*y + alfa*abs(signal[idx])
                anvelope.append(y)
                if idx > min_idx and tracking == True:                   
                    if y > max_a * threshold:
                        if ok==False:
                           start_idx = idx
                           ok=True 
                    elif ok == True:
                        end_idx = idx
                        tracking=False
                    
    return start_idx,end_idx,anvelope          
    
        
if __name__=="__main__":
    data = sys.stdin.read()
    
    file_handler=FileHandler()
    #file handler
    file_path = file_handler.select_file()
    #read dataframe
    data_frame, meta_data = get_data(file_path)
    #metadata
    Ts=meta_data["Sample Interval"]
    dc_component = 3.3/2
    #down sampling rate
    down_sample_rate = 1
    fs = 1/(Ts * down_sample_rate)
    #timestamps
    timestamps = np.array(data_frame.iloc[::down_sample_rate,0].to_list())
    #value
    voltages = np.array(data_frame.iloc[::down_sample_rate,1]) * 3.3/65535 - dc_component
    #period
    period = 0.001
    len_tx = int(period*fs)
    # Band-pass centered at 40 kHz
    low = 30100 / (fs / 2)
    high = 40100 / (fs / 2)
    b,a = butter( 2, [low, high], btype='bandpass', output='ba' )
    filtered_voltages = filtfilt(b,a,voltages)
    plt.figure()
    plt.plot(timestamps,voltages)
    #Hilbert detection by Anvelope
    start_idx , end_idx , anvelope,phase = detect_by_hilbert_anvelope_pipeline( filtered_voltages , timestamps , period , fs , min_time = 0.0015 , threshold = 0.25)
    rx_waveform = voltages[start_idx:end_idx]
    rx_timestamps = timestamps[start_idx:end_idx]
    plt.figure()
    plt.title( "Echo backscatter using hilbert" )
    plt.plot( rx_timestamps , rx_waveform )
    plt.show()
    plt.figure()
    plt.plot(timestamps , anvelope)
    plt.show()
    plt.figure()
    plt.plot(timestamps , phase)
    plt.show()
    
    plt.figure()
    rx_waveform_phase = phase[start_idx:end_idx]
    plt.plot( rx_timestamps , rx_waveform_phase )
    max_p = max(phase[start_idx:end_idx])
    min_p = min(phase[start_idx:end_idx])
    plt.show()
    plt.figure()
    plt.title("Some phase")
    start=50
    some_phase=phase[start:start+51]
    plt.plot(timestamps[start:start+51] , some_phase)
    plt.show()
    #Low-Pass + Redressed signal 
   
    start_idx_r,end_idx_r,anvelope_r = detect_by_rectified_anvelope_pipeline( voltages , timestamps , period , fs , min_time = 0.0015, threshold=0.25)
    rx_waveform_rectified = voltages   [start_idx_r : end_idx_r]
    rx_timestamps_rectified = timestamps [start_idx_r : end_idx_r]
    plt.figure()
    plt.title("Echo backscatter using rectified")
    plt.plot(rx_timestamps_rectified,rx_waveform_rectified)
    plt.show()
    
    plt.figure()
    plt.plot(timestamps , anvelope_r)
    plt.show()
    