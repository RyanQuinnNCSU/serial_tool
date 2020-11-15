from tkinter import *
from tkinter import ttk
import serial
from serial.tools import list_ports

# Globals
port_name = {}

class tkinter_setup:
    def __init__(self, root):
        root.title("Serial Hub")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        subFrame_mainFrame = ttk.Frame(root, padding="3 3 12 12")
        subFrame_mainFrame.grid(column=1, row=0, sticky=(N, W, E, S))
        button_subFrame_mainFrame_root = ttk.Button(subFrame_mainFrame, text="Calculate").grid(column=1, row=1, sticky=W)

        # feet = StringVar()
        # feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
        # feet_entry.grid(column=2, row=1, sticky=(W, E))
        #
        # meters = StringVar()
        # ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
        #
        # ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

        x = 1
        for dev_string in port_name:
            ttk.Label(mainframe, text=dev_string).grid(column=1, row=x, sticky=W)
            ttk.Label(mainframe, text=port_name[dev_string]).grid(column=2, row=x, sticky=W)
            x += 1

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        #feet_entry.focus()
        #root.bind("<Return>", calculate)

# def calculate(*args):
#     try:
#         value = float(feet.get())
#         meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
#     except ValueError:
#         pass

def list_ports():
    try:
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
    except Exception as e:
        print(e)
        sys.exit(1)



list_ports()




root = Tk()
tkinter_setup(root)
root.mainloop()
