import os
import sys
import io 
import subprocess
import serial
from serial.tools import list_ports


    
def main(argv):
    
    try:
        ports = list( serial.tools.list_ports.comports() )
        port_count = 0
        for port in ports:
            device_name = port.description
            if device_name.find('JLink CDC UART Port') != -1:
                start = device_name.find('COM')
                end = device_name.find(')',start)
                comport = device_name[start:end]
                print(comport)
                port_count += 1
        if port_count == 1:
             f = io.open('../tmp/gbl_info.txt', 'a', newline='\n')
             f.write(comport + "\n")
             f.close()
             os._exit(0)
        elif port_count == 0:
            os._exit(10)
        else:
            os._exit(20)
##        info = subprocess.STARTUPINFO()
##        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
##        info.wShowWindow = subprocess.SW_HIDE
##        output = subprocess.Popen(['chgport /QUERY'], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]
##        print(output)
        #out = subprocess.check_output(["chgport /QUERY"],shell=True)
        #print(out)
    
    except Exception as e:
        print(e)
        sys.exit(1)
        
if __name__ == "__main__":
   main(sys.argv[1:])
