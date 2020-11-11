import binascii
import datetime
import serial
import time
import os
import sys

def main(argv):
    got_com = False

    try:
        COM_port = str(sys.argv[1])
        ser = serial.Serial(COM_port, 115200, timeout=5 )
        print("Serial Open")
        get_address = b'\x20\x00\x01\x03'
        print("Transmitted gecko_cmd_system_get_bt_address")
        ser.write(get_address)
        response = ser.read(500)
        #response_decode = response.decode("hex")
        ser.close()
        print("Serial Closed")
        print(str(response))
        #Add bytes to GBL
        os.path.getsize(str(sys.argv[2]))
        
        sys.exit(0)      
    except Exception as e:
        print(e)
        sys.exit(1)
                

if __name__ == "__main__":
   main(sys.argv[1:])
