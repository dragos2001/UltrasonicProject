from machine import ADC,Timer,Pin
import time,sys
from array import array
import select
#count the samples
meas_counter = 0
#number of samples to collect/measurement
NUM_SAMPS = const(1000)

#initialize array
def get_array():
    data = array('H', ( 0 for _ in range(NUM_SAMPS)))
    return data

#sample data witha adc
def sample(data):
    index = 0
    adc = ADC(28)
    f = adc.read_u16
    t0 = time.ticks_us()
    while index < NUM_SAMPS:
        data[index] = f()
        index += 1
    t1 = time.ticks_us()
    td_us = time.ticks_diff(t1, t0)
    time_interval = td_us/(NUM_SAMPS * 1000000)
    #print(f'{td_us/NUM_SAMPS} us/conversion   {1000000*NUM_SAMPS/td_us} sps')
    return time_interval

#trigger sensor
def trigger():
    #trigger pin
    trigger_pin = Pin(10, Pin.OUT , Pin.PULL_DOWN)
    #echo pin
    echo_pin = Pin(11, Pin.IN , Pin.PULL_UP)                      
    #trigger
    trigger_pin.on()
    time.sleep_us(20)
    trigger_pin.off()

#extract analog waveform
# def extract_analog_waveform(data):
#     for 
    
#trig and measure
def collect_data(data, meas_obj, specs, counter):
    #trigger
    trigger()
    #measure
    ts = sample(data)
    #add to csv
    post_process_csv(meas_obj + "_" + str(counter) + "_" + specs + ".csv", data, ts)
    
def post_process_csv(path,samples,ts):
    with open(path,"w") as flog:
        flog.write("Timestamps")
        flog.write(",")
        flog.write("Voltages")
        flog.write("\r\n")
        for i in range(len(samples)):
            flog.write(f"{i*ts}")
            flog.write(str(","))
            k=samples[i]
            flog.write(f"{k}")
            flog.write("\r\n")
            
def read_measurement(meas_poll):
    if meas_poll.poll():
        string = sys.stdin.readline().strip()
        return string
    return None
    
def send_data_serial(data,ts):
    i=0
    #print(len(data))
    for i in range(len(data)):
        k=data[i]
        stamp=ts*i
        packet = '%f,%d' % (i*ts,k)
        print(packet)
        time.sleep(0.01)
        i+=1
     
meas_poll = select.poll()
meas_poll.register(sys.stdin , select.POLLIN)
while True:
    specs = read_measurement(meas_poll)
    if specs == "measure":
        print(f"Start Measurement {meas_counter}")
        data = get_array()
        #trigger sensor
        trigger()
        #Analog to Digital Conversion
        ts = sample(data)
        #Send the Data Serial
        send_data_serial(data,ts)
        post_process_csv("pole" + "_" + str(meas_counter) + "_" + specs + ".csv", data, ts)
    
        print(f"End Measurement {meas_counter}")
        meas_counter += 1
        time.sleep(1)
        
    

    
    





