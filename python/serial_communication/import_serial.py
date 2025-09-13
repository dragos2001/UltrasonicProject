from serial import Serial
from ..utils.utils import FileHandler
from ..processing.plot.plot_signal import plot_signal
import pandas as pd
import os
import time
PORT = 'COM8'  # Replace with your Pico's port
BAUDRATE = 115200
 
def read_from_pico_to_csv(file_path, serial_connection):
    #csv path
    timestamps=[]
    data_frame= pd.DataFrame(index = range(1500), columns=["Timestamps","Filtered Voltages","Envelope"])
    columns = data_frame.columns.tolist()
    col = 0
    row = 0
    while True:
        #check if input buffer
        if serial_connection.in_waiting:
           
            #read a line
            line = serial_connection.readline().decode('utf-8')
            #write to csv
            if "End Measurement" in line.strip():
                break
            elif "," not in line.strip():
                print(line)
            else:
                
                if row % 1500 == 0:
                    row = 0
                    col = col + 1
                    voltages = []

                elements = line.strip().split(",")
                array = list(map(float, elements))
                print(array)
                print(col)
                if col == 1:
                    data_frame.at[row, columns[col-1]] = array[0]
                data_frame.at[row, columns[col]] = array[1]
                row = row + 1

    data_frame.to_csv(file_path, index = False)        
    print("Excel created")
 
def get_measurement_dir():
        #directory
        root = os.getcwd()
        dir = os.path.join(root , "Measurements" , "Dataset")
        return dir
 
   
def main():
    fh = FileHandler()
    directory = fh.select_directory()
    #directory = get_measurement_dir()
    with Serial(PORT, BAUDRATE) as serial_connection:
        #Connected to port
        print(f"Connected to {PORT}")
        #Give the name of the object to measure
        obj = input("Give object's name: ")
        while True:
            # Read specifications of the measurement
            specs = input( "Give specs: ")
            if specs == "":
                break
            else:
                # Trigger measurerement
                serial_connection.write(("measure" + '\n').encode())
                # Start background thread to read Pico's responses
                path = f"{obj}_{specs}.csv"
                csv_path = os.path.join(directory,path)
                print(csv_path)
                read_from_pico_to_csv(csv_path, serial_connection)
                time.sleep(1)
                data = pd.read_csv(csv_path)
                plot_signal(data.iloc[:,0], data.iloc[:,1])
                time.sleep(1)
     
if __name__ == "__main__":
    main()
   