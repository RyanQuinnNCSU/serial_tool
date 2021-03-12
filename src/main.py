import tkinter as tk
from tkinter import ttk
# import serial
# from serial.tools import list_ports
import serial_functions as SF
import gui_classes as GUI
import os
import json

default_profile = {
    "Com Port": "COM3",
    "Baudrate": 115200,
    "Interval": 1.0,
    "Byte Format": "HEX",
    "Num_Commands": 3,
    "Commands": [
        {
            "name": "C1",
            "bytes": "0x01"
        },
        {
            "name": "C2",
            "bytes": "0x02"
        },
        {
            "name": "C3",
            "bytes": "0x03"
        }
    ]
}




try:
    template='{"Profile": "", "COM List": ["COM3: Silicon Labs CP210x USB to UART Bridge ", "COM4: Silicon Labs CP210x USB to UART Bridge ", "COM8: JLink CDC UART Port "]}'
    empty_config= json.loads(template)
    #print(empty_config['COM List'][0])
    dictionary ={
    "Profile" : "../json/default.json",
    "COM List" : [""]
    }
    if __name__ == "__main__":
        if not os.path.exists('../json'):#see if json folder exsit
            os.makedirs('../json')# iff not create file
        if not os.path.isfile("../json/config.json"):
            with open("../json/config.json", "w") as j_file:
                #empty_config = {"Profile": "", "COM List":[]}
                json.dump(dictionary,j_file)
                j_file.close()
            if not os.path.isfile("../json/default.json"):
                with open("../json/default.json", "w") as jp_file:
                    json.dump(default_profile,jp_file)
                    jp_file.close()
        SF.list_ports()
        app = GUI.SampleApp()
        if os.path.isfile("../Images/Bugger.ico"):
            app.iconbitmap("../Images/Bugger.ico")
        app.mainloop()
except Exception as e:
    print(e)
