import sys
import serial
from serial.tools import list_ports




def list_ports():
    try:
        port_name = {}
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            device_name = port.description
            end_of_discription = device_name.find("(COM")

            comport_s = device_name[end_of_discription+1:len(device_name)-1]
            discription = device_name[0:end_of_discription]
            print("*********")
            print(device_name)
            print(comport_s)
            print(discription)
            print("*********")
            port_name[comport_s] = discription
            # if device_name.find('USB to UART') != -1:
            #     start = device_name.find('COM')
            #     end = device_name.find(')', start)
            #     COM_port = device_name[start:end]
            #     print(COM_port)
        return port_name
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    list_ports()
