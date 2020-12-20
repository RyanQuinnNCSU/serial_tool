import sys
import serial
from serial.tools import list_ports
import json

config = {}

def list_ports():
    try:
        port_name = {}
        ports = list(serial.tools.list_ports.comports())
        with open("../json/config.json", "r") as read_file:
            config = json.loads(read_file.read())
            read_file.close()
        config['COM List'] = [] # clear com port list.
        iterator = 0
        for port in ports:
            iterator+=1
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
            config['COM List'].append(comport_s + ": " + discription) # device name hear.
        if(iterator == 0):
            config['COM List'].append("No Devices Detected") # device name hear.
        print(config)
        with open("../json/config.json", "w") as write_file:
            json.dump(config, write_file)
            write_file.close()
        return port_name

    except Exception as e:
        print(e)
        sys.exit(1)


def send_serial(bytes,com_port,baudrate):
    #remove '0x' from bytes
    byte_s1 = bytes.replace("0x", "")
    #remove ' ' from bytes
    byte_s2 = byte_s1.replace("0x", "")
    byte_2_send =  bytearray.fromhex(byte_s2)
    print("Bytes to send: " + str(byte_2_send))
    print("Com Port: " + com_port)
    print("Baudrate: " + str(baudrate))

    ser = serial.Serial(com_port, baudrate, timeout=5)
    print("Serial Open")
    print("Transmitted gecko_cmd_system_get_bt_address")
    ser.write(byte_2_send)
    response = ser.read(500)
    # response_decode = response.decode("hex")
    ser.close()
    print("Serial Closed")
    print("Serial Response = " + str(response))

if __name__ == "__main__":
    list_ports()
