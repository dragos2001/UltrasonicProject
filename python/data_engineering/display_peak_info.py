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
from envelope_feature_extraction import flat_dict
import matplotlib.cm as cm
    
if __name__=="__main__":
    
    #read data
    MARGIN = 20
    PEAK = 0.05
    
    n_properties = 2
    fh = FileHandler()
    dir_path = fh.select_file()
    envelope_dataset = pd.read_csv(dir_path, index_col = 0)
    
    features = ["max amp","std","kurtosis","skewness","power","rise time","fall time","peak entropy"]
    features.extend(envelope_dataset.columns[-7:])
    

    
    #features_dataset, properties_dataset = extract_features(envelope_dataset, features, MARGIN, PEAK, n_properties, dir_path)
    for index, row in envelope_dataset.iterrows():
        envelope = row[:201].values
        ax = plot_signal( np.arange(0, len(envelope)), envelope, title = index )
        peaks_indices,  properties = find_peaks(
         envelope, 
         height=PEAK, 
         threshold = (None,None),
         distance=MARGIN, 
         prominence=(None,None),
         width= (None,None),
         rel_height=1,
         plateau_size = (None,None) )
        
        #sort
        sorted_indices = np.flip(np.argsort(properties["peak_heights"]))
        sorted_properties = { key : properties[key][sorted_indices] for key in properties.keys() }
        reduced_properties = flat_dict(sorted_properties, n_properties)       
        ax.stem(peaks_indices, properties["peak_heights"],linefmt = 'red', markerfmt='red')
        num_peaks = len(peaks_indices)
        num_colors = 2*num_peaks
        colors = ["green","blue","yellow","turquoise"]
        # Plot left_ips and right_ips
        for i in range (min(len(sorted_indices),n_properties)):
           
            ext = f" {i+1}"
      
                
            ax.plot(reduced_properties["left_ips"+ext], envelope[int(reduced_properties["left_ips"+ext])], marker='o',color = colors[2 * i], label="Left IPs"+ext)
            ax.plot(reduced_properties["right_ips"+ext], envelope[int(reduced_properties["right_ips"+ext])], marker ='o',color = colors[(2 * i)+1], label="Right IPs"+ext)

            ax.plot(reduced_properties["left_bases"+ext], envelope[reduced_properties["left_bases"+ext]], marker='^',color = colors[2 * i] , label = "Left Bases"+ext)
            ax.plot(reduced_properties["right_bases"+ext], envelope[reduced_properties["right_bases"+ext]], marker='^',color = colors[(2 * i) + 1], label = "Right Bases"+ext)
         
          
                
                
                
        # Annotate widths
        for i in sorted_indices:
            if i < n_properties:
                width = properties["widths"][i]
                ax.annotate(f"w={width:.2f}", xy=(peaks_indices[i], envelope[peaks_indices[i]]), xytext=(peaks_indices[i], envelope[peaks_indices[i]]+0.02),
                            textcoords="data", fontsize=8, color='purple')

        ax.set_title(f"Peak Properties for Signal: {index}")
        ax.set_xlabel("Sample Index")
        ax.set_ylabel("Amplitude")
        ax.legend()
        plt.tight_layout()
        plt.show()
    
    
    
    