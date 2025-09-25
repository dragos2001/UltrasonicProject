# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 13:59:42 2025

@author: BRD5CLJ
"""
from utils import FileHandler
import pandas as pd
import os 
import matplotlib.pyplot as plt

def plot_compare(filt, env, title):
    plt.plot(filt,color='blue')
    plt.plot(env, color='red')
    plt.title(title)
    plt.show()
    
if __name__ == "__main__":
    
    fh = FileHandler()
   
    #select root directory
    dir_path =  fh.select_directory("Directory Path")
    
    filtered_dataset_path = os.path.join(dir_path,"dataset_ultrasonic_sensor_filtered.csv")
    envelope_dataset_path = os.path.join(dir_path,"dataset_ultrasonic_sensor_envelope.csv")
    
    dataframe_envelope = pd.read_csv(envelope_dataset_path)
    dataframe_filtered = pd.read_csv(filtered_dataset_path)
    
    for index, filt_voltages in dataframe_filtered.iterrows():
            title = dataframe_envelope.iloc[index][0]
            envs =  dataframe_envelope.iloc[index][1:202].values
            filts = filt_voltages.iloc[1:].values
            diff =  filts[0] - envs[0]
            filts = filts-diff
            plot_compare(filts,envs,title)
         
     
     