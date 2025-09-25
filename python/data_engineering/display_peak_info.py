# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 11:19:56 2025

@author: BRD5CLJ
"""

from utils import FileHandler
import pandas as pd
from envelope_feature_extraction import peaks_norm_entropy
from plot_signal import plot_signal
from envelope_feature_extraction import extract_features
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import keyboard
import threading
import time 
import sys

paused = False

def pause_process():
    
    global paused
    
    for line in sys.stdin:
        print(line.strip)
    if keyboard.is_pressed('space'):
        paused = not paused
        print("pause" if paused else "resume")
        time.sleep(1)
    elif keyboard.is_pressed('esc'):
        print("exit")
        return False
        
def plot_peak_characteristics(properties_row):
    
    for elem in properties_row:
        return
    
    
if __name__=="__main__":
    
    #read data
    MARGIN = 20
    PEAK = 0.05
    
    n_properties = 1
    fh = FileHandler()
    dir_path = fh.select_file()
    envelope_dataset = pd.read_csv(dir_path, index_col = 0)
    
    features = ["max amp","std","kurtosis","skewness","power","rise time","fall time","peak entropy"]
    features.extend(envelope_dataset.columns[-7:])
    
    x = threading.Thread( target = pause_process,daemon=True)
    x.start()
    
    #features_dataset, properties_dataset = extract_features(envelope_dataset, features, MARGIN, PEAK, n_properties, dir_path)
    for index, row in envelope_dataset.iterrows():
        while paused == True:
            time.sleep(2)
        envelope = row[:201].values
        ax = plot_signal( np.arange(0, len(envelope)), envelope, title = index )
        peaks_indices, indices,  properties = find_peaks(envelope, height=PEAK, threshold = (None,None), distance=MARGIN, prominence=(None,None), width= (None,None), rel_height=1,plateau_size = (None,None) )
        
        #sort
        sorted_indices = np.argsort(properties["peak_heights"])
        sorted_properties = { key : properties[key][sorted_indices] for key in properties.keys() }
        ax.stem(peaks_indices,properties["peak_heights"],linefmt = 'red', markerfmt='red')
        plt.show()
    
    
    
    
    