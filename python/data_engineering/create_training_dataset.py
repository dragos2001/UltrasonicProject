# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 15:42:28 2025

@author: BRD5CLJ
"""

from utils import FileHandler
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from plot_signal import plot_signal
import matplotlib.pyplot as plt

def compose_summary(metadata):
    text_list=[]
    text_list.append(f"Total number of measurements: {metadata[0]}")
    text_list.append(f"Validated number of measurements: {metadata[1]}")
    text_list.append(f"Invalidated number of measurements: {metadata[2]}")
    text_list.append(f"Number of short measurements: {metadata[3]}")
    text_list.append(f"Number of tall measurements: {metadata[4]}")
    return text_list

def write_summary(dataset_path,text_list):
    with open(dataset_path[:-4] + "_summary.txt", "w") as f:
        for line in text_list:
            f.write(line+'\n')
            print(line)
        
    
def extract_relevant_signal_peaked_centered(array,threshold,margin): 
    max_val=0
    length=int(len(array)-margin/4)
    for i in range (int(2*margin),length):
        if array[i]>max_val:
            max_val=array[i]
            origin=i
    
    if max_val>threshold:
        if origin-margin > 2*margin:
            if origin+margin<length:
                 left_margin = origin-margin
                 right_margin= origin +margin
            
            else:
                 right_margin = len(array) - int(margin/10)
                 left_margin = len(array) - int(margin/10) - 2*margin
        else:
            left_margin = origin - int(margin/2)
            right_margin = origin+ 3*int(margin/2)

        extracted=[]
        for i in range(left_margin,right_margin+1):
                extracted.append(array[i])
            
        return (extracted,origin,max_val,left_margin)
    
    return None


if __name__ =="__main__":
    
    fh = FileHandler()
    #parametrization
    MARGIN = 100
    THRESHOLD = 0.05
    
    #select root directory
    main_dir_path = fh.select_directory("Measurements dir")
    dataset_dir = fh.select_directory("dataset_envelope_features dir")
    
    #create column names
    column_samples = [f"sample_{i}" for i in range(1, 2 * (MARGIN+1))]
    features = ["distance","grid_x","grid_y","angle","real_x","real_y","label"]
    column_names = column_samples + features
    
    #create dataset_envelope_features
    dataset_envelope_features = pd.DataFrame(columns = column_names)
    dataset_signal_filtered = pd.DataFrame(columns = column_samples )
    
    #scaler for normalization
    scaler_env = MinMaxScaler(feature_range = (0, 1))
    scaler_filt = MinMaxScaler(feature_range = (-1, 1))
    
    #count measurements
    count = 0
    i_count = 0
    v_count = 0
    n_tall = 0
    n_short = 0
    
    #indexes corresponding to the name of each measurement
    meas_indexes = []
    
    #initialize the global minimum
    global_min_amp = 1
    
    #iterate over directories in root
    for obj_dir_name in os.listdir(main_dir_path):
        
        #create paths
        obj_dir_path = os.path.join(main_dir_path, obj_dir_name)
        
        #iterate over the files
        for filename in os.listdir(obj_dir_path):
            if filename.endswith("filtered.csv"):
                
                #count total number of measurements
                count = count+1
               
                #create csv path
                measurement_path = os.path.join(obj_dir_path,filename)
                
                #read dataframe
                current_measurement = pd.read_csv(measurement_path)
    
                #extract series
                measurement_envelope = current_measurement["envelope"]
                measurement_filt_signal = current_measurement["filtered_signal"]
                
                #extract values
                envelope_values = measurement_envelope.values
                filtered_values = measurement_filt_signal.values
                
                #scale envelope values
                envelope_values_scaled = scaler_env.fit_transform(envelope_values.reshape(-1,1),y = None).flatten()
                filtered_values = scaler_filt.fit_transform(filtered_values.reshape(-1,1), y = None).flatten()
                
                #extract ref object waveform
                output = extract_relevant_signal_peaked_centered(envelope_values_scaled, THRESHOLD , MARGIN)
                
                #verify for valid measurement
                if output != None:
                    #increment + extract waveform
                    v_count = v_count+1
                    #extracted envelope
                    extracted_envelope_values_scaled = output[0]
                    #origin
                    origin = output[1]
                    #max amp
                    meas_max_amp = output[2]
                    #left margin
                    left_margin=output[3]
                    #extracted filtered values
                    extracted_filtered_values_scaled = filtered_values[left_margin : left_margin + 2*MARGIN+1]
                    
                    #compute the global minimum of all measurementss
                    if meas_max_amp < global_min_amp:
                        global_min_amp = meas_max_amp
                        global_min_envelope = extracted_envelope_values_scaled
                        global_min_origin = origin-left_margin
                    
                    current_index = obj_dir_name + '_' + filename
                    
                    #append measurement to indexes
                    meas_indexes.append(current_index)
                    
                    #compute the distance
                    distance = 343*(origin * 0.00000811)/2
                    
                    #extract positioonal information                    
                    grid_x =  current_measurement["grid_x"][0]
                    grid_y = current_measurement["grid_y"][0]
                    angle = current_measurement["angle"][0]
                    real_x = current_measurement["real_x"][0]
                    real_y = current_measurement["real_y"][0]
                    label = current_measurement["type"][0]
                    
                    #count labels
                    if label == 'tall':
                        n_tall+=1
                    else:
                        n_short+=1                        
                    
                    #concatenate features
                    measurement_row_envelope = pd.concat([pd.Series(extracted_envelope_values_scaled), pd.Series([distance,grid_x,grid_y,angle,real_x,real_y,label])], axis = 0)
                    measurement_row_values_filtered = pd.Series(extracted_filtered_values_scaled)
                   
                    
                    #transform to dataframes
                    measurement_row_envelope = measurement_row_envelope.to_frame().T
                    measurement_row_envelope.columns = dataset_envelope_features.columns
                    measurement_row_envelope.index = [current_index]
                    measurement_row_values_filtered = measurement_row_values_filtered.to_frame().T
                    measurement_row_values_filtered.columns = column_samples
                    measurement_row_values_filtered.index = [current_index]
                    
                    #concatenate dataframes
                    dataset_envelope_features = pd.concat([measurement_row_envelope, dataset_envelope_features], axis = 0)
                    dataset_signal_filtered = pd.concat([measurement_row_values_filtered, dataset_signal_filtered], axis = 0)
                    
                else:
                    #increment invalid number of invalid measurements
                    i_count=i_count+1
                    
    #set dataset_envelope_features index column to meas name              
    #dataset_envelope_features.set_index = meas_indexes
    #dataset_signal_filtered.index = meas_indexes
    
    #plot the smallest envelope
    axis = plot_signal(np.arange(0,len(global_min_envelope)), global_min_envelope, "Envelope plot with the minimum extracted envelope",color = 'blue')
    axis.plot(np.arange(0,len(global_min_envelope)), [THRESHOLD]*len(global_min_envelope),color='red')
    plt.show()
    
    #export dataset to csv
    dataset_path = os.path.join( dataset_dir,"dataset_ultrasonic_sensor")
    dataset_envelope_features.to_csv(dataset_path + "_envelope.csv")
    dataset_signal_filtered.to_csv(dataset_path + "_filtered.csv")
    
    #export metadata
    metadata = [count,v_count,i_count,n_short,n_tall]
    summary = compose_summary(metadata)
    write_summary(dataset_path,summary)
    
    