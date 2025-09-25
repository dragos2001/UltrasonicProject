# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 17:01:01 2025

@author: BRD5CLJ
"""
import numpy as np
import matplotlib.pyplot as plt
from utils import FileHandler
import os 
import pandas as pd
from plot_signal import plot_signal
from scipy.signal import find_peaks
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif

#normnalization function
def normalize_dataset(dataframe,scaler):
    for col in dataframe.columns:
        dataframe[col] = scaler.fit_transform(np.array(dataframe[col]).reshape(-1,1))
        

       
def corr_matrix(dataframe,title="Corr Matrix"):
    correlation_matrix = dataframe.corr()
    # Plotting the correlation matrix as a heatmap
    plt.figure(figsize=(20, 20))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.1)
    
    plt.title(title)
    plt.show()

def max_envelope_amp(signal):
    max_v = 0
    for i,v in enumerate(signal):
        if v > max_v:
            max_v = v
            pos = i
    
    return max_v, pos
 

def power(signal):
    energy = 0
    for i,v in enumerate(signal):
        energy = energy + v
    
    return energy/i
    

def rise_time(signal):
    max_v, pos = max_envelope_amp(signal)         
    th1 = 0.9 * max_v
    th2 = 0.35 * max_v
    ok = False
    
    for i in range(pos,-1,-1):
        if signal[i] <= th1 and ok == False:
                up = i
                ok=True
                
        if signal[i] <= th2 and ok == True:
                down = i
                break
    return up-down
    
 
def fall_time(signal):
    max_v,pos=max_envelope_amp(signal)         
    th1 = 0.9 * max_v
    th2 = 0.35* max_v
    ok = False
    
    for i in range(pos,len(signal)):
        
        if signal[i] <= th1 and ok == False:
                up = i
                ok=True
                
        if signal[i] <= th2 and ok == True:
                down = i
                break
    return down-up

def mean(array):
    mean=0
    for x,f in enumerate(array):
        mean = mean + x*f
        
    return mean
    

def std(array):
    u = mean(array)
    std = 0 
    for x,f in enumerate(array):
        std = std + (x-u)*(x-u)*f
    
    std = np.sqrt(std)
    return std
  
    
def skewness(array):
    std_v = std(array)
    m_v = mean(array)
    m_3 = 0
    for x,f in enumerate(array):
        val = x - m_v
        m_3 = m_3 + val**3 * f
        
    sk = m_3 / std_v**3
    return sk

def kurtosis(array):
    std_v = std(array)
    m_v = mean(array)
    m_4 = 0
    for x,f in enumerate(array):
        val = x - m_v
        m_4 = m_4 + val**4 * f
    
    ku = m_4 / std_v**4
    return ku
            
def peaks_norm_entropy(array,height,distance):
    peaks, properties = find_peaks(array, height=height, threshold = (None,None), distance=distance, prominence=(None,None), width= (None,None), rel_height=1,plateau_size = (None,None) )
    peaks_amp = properties['peak_heights']
    peak_max = max(peaks_amp)
    peak_entropy = 0
    for peak in peaks_amp:
        peak_norm = peak / peak_max
        peak_entropy = peak_entropy + peak_norm * np.log(peak_norm)
    
    return -peak_entropy,peaks, properties


def flat_dict(initial_dict,max_len=3):
    flatten_dict={}
    for key,value in initial_dict.items():
        for i in range(0, max_len):
            if i < len(value):
                flatten_dict[f"{key} {i+1}"] = value[i]
            else:
                flatten_dict[f"{key} {i+1}"] = 0

    return flatten_dict

def handle_error(e,envelope,index_meas):
    print(e)
    #plot signal
    plot_signal(np.arange(0,len(envelope)),envelope,title="Envelope generating error")
    dir_meas,meas_name = index_meas.split('cm')
    dir_meas = dir_meas + 'cm'
    meas_name = meas_name[1:]
    dir_data = os.path.dirname(dir_path)
    err_dir_meas_path = os.path.join(dir_data,"All_Data",dir_meas,meas_name)
    err_dataframe = pd.read_csv(err_dir_meas_path)
    plot_signal( np.arange(0,len(err_dataframe["envelope"])), err_dataframe["envelope"], title = "Erronous envelope data")
    max_v = max(envelope)
    min_v = min(envelope)
    return max_v,min_v
    

def extract_features(envelope_dataset, features, MARGIN, PEAK, n_properties, dir_path):
     #features dataset
     features_dataset = pd.DataFrame(data = envelope_dataset, index = envelope_dataset.index , columns = features)
     
     #initialize lists
     max_amp_values=[]
     std_values=[]
     kurtosis_values=[]
     skewness_values=[]
     power_values=[]
     rise_time_values=[]
     fall_time_values=[]
     peaks_entropy=[]
     properties = []
     
     #iterate over rows in envelope dataset
     for index_meas, row in envelope_dataset.iterrows():
        
         try:
             #extract envelope
             envelope = row[:201].values
             #max amplitudes
             max_amp_values.append(max_envelope_amp(envelope)[0])
             #stadard deviations
             std_values.append(std(envelope))
             #kurtosis values
             kurtosis_values.append(kurtosis(envelope))
             #skewness values
             skewness_values.append(skewness(envelope))
             #power values
             power_values.append(power(envelope))
             #rise time values
             rise_time_values.append(rise_time(envelope))
             #fall time values
             fall_time_values.append(fall_time(envelope))
             #entrop and other topographic proeprties
             entropy, peaks_indices, props = peaks_norm_entropy(envelope, height = PEAK, distance = MARGIN)
             #sort
             sorted_indices = np.argsort(props["peak_heights"])
             sorted_properties = { key : props[key][sorted_indices] for key in props.keys() }
             properties.append(sorted_properties)
             peaks_entropy.append(entropy)
         
         #in case of error 
         except (UnboundLocalError) as e:
             handle_error(e, envelope, index_meas)
             break  
         
     #assign columns
     features_dataset["max amp"] = max_amp_values
     features_dataset["std"] = std_values
     features_dataset["kurtosis"] = kurtosis_values
     features_dataset["skewness"] = skewness_values
     features_dataset["power"] = power_values
     features_dataset["rise time"] = rise_time_values
     features_dataset["fall time"] = fall_time_values
     features_dataset["peak entropy"] = peaks_entropy
     #categorical->numeric
     features_dataset['label'] = (features_dataset['label']=='tall').astype(int)  
     #flat properties
     flattened_properties = [flat_dict(d,n_properties) for d in properties]
     #df properties
     properties_dataset = pd.DataFrame(flattened_properties, index = features_dataset.index)
     properties_dataset['label'] = features_dataset['label']
     
     
     return features_dataset, properties_dataset
     
    
    
    
if __name__ == "__main__":
    
    MARGIN = 20
    PEAK = 0.05
    n_properties = 1
    fh = FileHandler()
    dir_path = fh.select_directory(title="Dataset dir")
    dataset_path_list = []
    for dataset_name in os.listdir(dir_path):
        dataset_path = os.path.join(dir_path,dataset_name)
        ext = dataset_path[-3:]
        if ext == 'csv':
            dataset_path_list.append(dataset_path)
        
    envelope_dataset = pd.read_csv(dataset_path_list[0], index_col = 0)
    
    features = ["max amp","std","kurtosis","skewness","power","rise time","fall time","peak entropy"]
    features.extend(envelope_dataset.columns[-7:])
    #features dataset
    features_dataset, properties_dataset = extract_features(envelope_dataset, features, MARGIN, PEAK, n_properties, dir_path)
    #apply normalzation
    scaler = MinMaxScaler()
    normalize_dataset(properties_dataset, scaler)
    normalize_dataset(features_dataset, scaler)
    #extend dataset
    features_dataset_extended = pd.concat([features_dataset, properties_dataset], axis = 1)
    #move label at the end
    features_dataset_extended = features_dataset_extended[[col for col in features_dataset_extended if col != "label"]]
    features_dataset_extended["label"] = features_dataset["label"]
    #corr matrix
    corr_matrix(features_dataset, title = "Envelope features corr matrix")
    corr_matrix(properties_dataset, title = "Envelope properties corr matrix")
    corr_matrix(features_dataset_extended, title = "Envelope properties ext corr matrix")
    features_dataset_extended.to_csv(os.path.join(dir_path, "dataset_extended_envelope_features.csv"))
    