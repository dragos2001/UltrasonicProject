import serial
import sys
import time

def receive_command(communication):
    command = communication.read_until()
    return command.decode('utf-8')

def send_command(communication):
    text = input()
    command = "%s\n" % (text)
    print("TX command:",command)
    communication.write(command.encode('utf-8'))
    return text

if __name__=="__main__":
    communication=serial.Serial('COM5', baudrate = 9600)
    #object name
    print("Give object:")
    object_name = send_command(communication)

    while True:
        #Specifications of the measurement
        print("Give meas specs:")
        specs = send_command(communication)

        #Receive status
        status= receive_command(communication)
        print("RX command:",status)

       
        data= receive_command(communication)
        print("Line:",data)
        time.sleep(0.01)
        



    