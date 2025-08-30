import serial
import threading
import os
import time
PORT = 'COM5'  # Replace with your Pico's port
BAUDRATE = 115200

def read_from_pico_to_csv(directory, filename, serial_connection):
    #csv path
    csv_path = os.path.join(directory,filename)
    with open (csv_path, mode="w",newline='') as file:
        file.write("Timestamps,Voltages\r\n")
        while True:
            #check if input buffer
            if serial_connection.in_waiting:
                #read a line
                line = serial_connection.readline().decode('utf-8')
                #write to csv
                if "Start" in line.strip():
                    print("--Start csv---")
                elif "End" in line.strip():
                    print("---End csv---")
                    break
                #write line
                else:
                    print(line)
                    file.write(line.strip()+"\n")
                           
    print("Excel created")

def get_measurement_dir():
        #directory
        root = os.getcwd()
        dir = os.path.join(root , "Measurements" , "Dataset")
        return dir

    
def main():
    directory = get_measurement_dir()
    with serial.Serial(PORT, BAUDRATE) as serial_connection:
        #Connected to port
        print(f"Connected to {PORT}")
        #Give the name of the object to measure
        obj = input("Give object's name: ")
        while True:
            # Read specifications of the measurement
            specs = input( "Give specs: ")
            # Trigger measurerement
            serial_connection.write(("measure" + '\n').encode())
            # Start background thread to read Pico's responses
            read_from_pico_to_csv(directory, f"{obj}_{specs}.csv", serial_connection , ) 
            time.sleep(1)
      
if __name__ == "__main__":
    main()