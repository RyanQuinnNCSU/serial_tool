# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import serial
import os
import sys
import time
import serial
from serial.tools import list_ports

def test_serial():
    # Use a breakpoint in the code line below to debug your script.
    try:
        ports = list(serial.tools.list_ports.comports())
        port_count = 0
        for port in ports:
            device_name = port.description
            print(device_name)
            if device_name.find('USB to UART') != -1:
                start = device_name.find('COM')
                end = device_name.find(')', start)
                COM_port = device_name[start:end]
                print(COM_port)
                port_count += 1
        if port_count >= 1:
            ser = serial.Serial("COM13", 115200, timeout=5)
            print("Serial Open")
            get_address = b'\x20\x00\x01\x03'
            print("Transmitted gecko_cmd_system_get_bt_address")
            ser.write(get_address)
            response = ser.read(500)
            # response_decode = response.decode("hex")
            ser.close()
            print("Serial Closed")
            print(str(response))
            os._exit(0)
        else:
            os._exit(20)
    ##        info = subprocess.STARTUPINFO()
    ##        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    ##        info.wShowWindow = subprocess.SW_HIDE
    ##        output = subprocess.Popen(['chgport /QUERY'], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]
    ##        print(output)
    # out = subprocess.check_output(["chgport /QUERY"],shell=True)
    # print(out)

    except Exception as e:
        print(e)
        sys.exit(1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_serial()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
