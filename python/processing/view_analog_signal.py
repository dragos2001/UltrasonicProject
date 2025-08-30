import matplotlib.pyplot as plt
import pandas as pd
import csv
import numpy as np
from scipy.signal import correlate
from math import ceil
from utils import FileHandler
#get data
def get_data(file_path):
    n_rows=0
    metadata={}
    with open(file_path) as fd:
        csv_reader=csv.reader(fd,delimiter=',')  
        while True:
            current_row = next(csv_reader)
            print(current_row)
            if current_row:
                if ("Voltages" == current_row[1] and 'Timestamps' == current_row[0]):
                        time1 = next(csv_reader)[0]
                        time2 = next(csv_reader)[0]
                        print(next(csv_reader))
                        print(time2 , " - " , time1)
                        Ts = np.float32(time2)-np.float32(time1)
                        metadata["Sample Interval"] = Ts
                        break
                        
                elif ("Sample Interval" == current_row[0]):
                        Ts = np.float32(current_row[1])
                
                metadata[current_row[0]]=current_row[1]
                    
                n_rows = n_rows+1
            else: break
    #read dataframe
    data_frame = pd.read_csv( file_path, skiprows=n_rows , usecols=["Timestamps","Voltages"], sep=",",dtype=np.float64)
    return data_frame, metadata
    
    
def get_correlation_coefficients(signal1,signal2):
    #compute the reference signal 
    template=signal2.copy()
    #define circular buffer size
    buffer_size=len(template)
    #create empty buffer
    buffer=np.zeros(len(template))
    #correlation coefs
    correlation_coefs=np.array([])
    #position to occupy in the buffer
    index=0
    #iterate over the hole signal
    signal_energy = np.dot(signal2,signal2)
    #min and max
    min_c = 1
    max_c = 0
    
    for i in range( 0 , len(signal1) - 1):
        #assign value to current position
        buffer[index] = signal1[i]
        #initialize variables
        corr = 0
        if i > buffer_size-1:
    
            sum_template = 0
            sum_buffer = 0
            #compute correlation
            for j in range(0 , len(signal2) - 1):
                corr = corr + template[j] * buffer[(buffer_size + j - index) % buffer_size];           
            
            L2_buffer = np.linalg.norm(buffer)
            L2_template =  np.linalg.norm(template)    
            #if L2_buffer > 5:
            corr = abs( corr / (L2_buffer * L2_template))
# =============================================================================
#             if corr > max_c:
#                 max_c = corr
#             if corr < min_c:
#                 min_c = corr 
#             corr = corr / signal_energy
#             #else :
#                 #corr = 0
# =============================================================================
                    
        correlation_coefs=np.append(correlation_coefs,corr)
        #update index
        index = (index+1) % buffer_size
        

    #correlation_normalized = (correlation_coefs - min_c) / (max_c - min_c)    
    return correlation_coefs

def get_energy(signal1,signal2):
    #buffer size
    buffer_size = len(signal2)
    #correlation coefs
    padding = np.zeros(len(signal2)-1)
    signal1 = np.concatenate( (padding,signal1) , axis=0)
    energy_windows = []
    #iterate over the hole signal
    for i in range( 0 , len(signal1) - buffer_size):
        #current signal
        current_signal = signal1[i:i+buffer_size]
        dot_product =  np.dot(current_signal,current_signal)
        #compute Norms
        energy = np.linalg.norm(dot_product)
        energy_windows.append(energy)
    #energy template   
    energy_template=np.dot(signal2,signal2)
    return energy_windows,energy_template

def get_correlation_normalized(signal1,signal2):
    #buffer size
    buffer_size=len(signal2)
    #compute the reference signal 
    template=signal2.copy()
    #padding
    padding = np.zeros(len(signal2)-1)
    #correlation coefs
    correlation_coefs=[]
    #position to occupy in the buffer
    signal_energy=np.dot(template,template)
    #concatenate
    signal1=np.concatenate((padding,signal1),axis=0)
    #iterate over the hole signal
    for i in range( 0 , len(signal1)-buffer_size):
        #current signal
        current_signal = signal1[i:i+buffer_size]
        corr =  np.dot(current_signal,template)
        #compute Norms
        L2_buffer = np.linalg.norm(current_signal)
        L2_template =  np.linalg.norm(template)
        #corr= corr / signal_energy
    
        corr= corr / (L2_buffer* L2_template)
        
       
        correlation_coefs.append(corr)
    
    
    return correlation_coefs
def get_tx_voltages(timestamps,voltages, finish_time=0.001):
    start=-1
    i = 0
    tx_voltages=[]
    while True:
        
        if timestamps[i] >= 0 and timestamps[i] < finish_time:
            if start == -1:
                   start=i 
            tx_voltages.append(voltages[i])
           
        elif timestamps[i] >= finish_time:
            break
        
        i=i+1
        
    return start , np.array(tx_voltages)

if __name__=="__main__":
    #file handle
    file_handle=FileHandler()
    #downsample rate
    down_sample_rate=1
    #process metadata
    file_path = file_handle.select_file()
    #data frame
    data_frame,metadata = get_data(file_path)
    #data_frame = pd.read_csv( file_path, usecols=["Timestamps","Voltages"], sep=",",dtype=np.float64)
    #dc component
    dc_component =3.33/2
    #down sampling rate
    down_sample_rate=1
    #sampling rate
    ts = metadata["Sample Interval"] 
    fs = 1/ (down_sample_rate*ts)
    #timestamps
    timestamps = np.array(data_frame.iloc[::down_sample_rate,0].to_list(),dtype=np.double)
    #value
    #voltages = np.array(data_frame.iloc[::down_sample_rate,1].to_list()) * 3.3 / 65536
    voltages = np.array(data_frame.iloc[::down_sample_rate,1].to_list())
    #voltages = [x - 3.3/2 for x in voltages]
    
    plt.figure()
    plt.plot(timestamps,voltages,'r')
    plt.show()
    
    #---------------------- Time Analysis --------------------------------------------------------
    
    plt.figure()
    axs1 = plt.subplot(311, title ="Cycle Measurement")
    axs1.plot(timestamps , voltages , 'r')
    #determine tx signal
    pulse_period = 0.002 #us
    number_of_samples = int(pulse_period* fs ) #number of samples
    #tx voltages
    axs2 = plt.subplot(312, title ="Tx signal")
    start_index, tx_voltages = get_tx_voltages( timestamps , voltages , finish_time =  pulse_period)
    axs2.plot(timestamps[ start_index : start_index + len(tx_voltages) ] , tx_voltages)   
    
    #rx voltages
    axs3 = plt.subplot(313, title ="Rx signal")
    start_rx =int( (fs * 0.00258) + start_index)
    end_rx = start_rx + len(tx_voltages)
    rx_voltages = voltages[ start_rx : end_rx ]
    axs3.plot(timestamps[ start_rx : end_rx ] , rx_voltages)   
    #prior
    time_moment=0.005
    start_noise = int(time_moment*fs)
    #noise seq
    noise_seq = voltages[start_noise : start_noise + number_of_samples ]
    sigma=np.std(noise_seq)
    
    #-------------------- Correlation Analysis ------------------------------------
    
    #correlation
    beta = 1/ (sigma*np.sqrt(np.dot(tx_voltages,tx_voltages)))
    correlation = correlate(voltages, beta * tx_voltages,"same")
    correlation_coefs = get_correlation_coefficients(voltages,tx_voltages)
    correlation_norm_coefs = get_correlation_normalized(voltages,tx_voltages)
    #figure
    plt.figure()
    axs3 = plt.subplot(211, title ="Correlation Pythonic")
    axs3.plot(timestamps[:-1],correlation_norm_coefs,'b')
    axs4 = plt.subplot(212, title ="Correlation DSP")
    axs4.plot(timestamps[:-1],correlation_coefs,'b')
  
    
    #------------Fourier Analysis--------------------------------------------
    
    #figure
    plt.figure()
    #Axs 5- analog signal
    axs5 = plt.subplot(411, title ="Spectrum Analog Signal")
    n = len(voltages)
    k = np.arange(n)
    T = n / fs
    #frequency
    frq = k/T
    frq = frq[:len(frq)//2]
    #spectrum
    Y = np.fft.fft(voltages) / n#dft and normalization
    Y = abs(Y[:n//2])
    axs5.plot(frq , Y , 'r')
    
    #Axs 6 - noise 
    axs6 = plt.subplot(412, title ="Spectrum noise")
    n = len(noise_seq)
    k = np.arange(n)
    T = n / fs
    #frequency
    frq = k/T
    frq = frq[:len(frq)//2]
    #spectrum
    Y = np.fft.fft(noise_seq) / n # dft and normalization
    Y = abs(Y[:n//2])
    axs6.plot(frq , Y , 'r') 
    
    #Axs 7 - rx signal
    axs7 = plt.subplot(413, title ="Spectrum rx")
    n = len(rx_voltages)
    k = np.arange(n)
    T = n / fs
    #frequency
    frq = k/T
    frq = frq[:len(frq)//2]
    #spectrum
    Y = np.fft.fft(rx_voltages) / n # dft and normalization
    Y = abs(Y[:n//2])
    axs7.plot(frq , Y , 'r')
    
    #Axs 8 - tx signal
    axs8 = plt.subplot(414, title ="Spectrum tx")
    n = len(tx_voltages)
    k = np.arange(n)
    T = n / fs
    #frequency
    frq = k/T
    frq = frq[:len(frq)//2]
    #spectrum
    Y = np.fft.fft(tx_voltages) / n # dft and normalization
    Y = abs(Y[:n//2])
    max_tx_A=max(Y)
    axs8.plot(frq , Y , 'r')
    plt.subplots_adjust(hspace = 1)
    plt.show()
    
    #------Signal Energy-----------
    energy_windows, energy = get_energy(voltages , tx_voltages) 
    plt.figure()
    plt.plot(timestamps[:-1],energy_windows)
    plt.show()
    
    
