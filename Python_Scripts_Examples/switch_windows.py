# Multi-frame tkinter application v2.3
import tkinter as tk
from tkinter import ttk
import serial
from serial.tools import list_ports

# Globals
port_name = {}

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Com_viewer)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

class Com_viewer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("COM Viewer")
        x = 1 #row number
        w = 350
        h = 500
        ws = master.winfo_screenwidth() # width of the screen
        hs = master.winfo_screenheight() # height of the screen

        master.geometry("%dx%d+%d+%d" % (w,hs,ws-w,0))
        self.grid(column=0, row=0, sticky='NWES')
        tk.Label(self, text="COM Port #",borderwidth=5, relief="groove",font=("Courier",10,"bold")).grid(column=1, row=x, sticky='W')
        tk.Label(self, text="Device Discription",borderwidth=5, relief="groove",font=("Courier",10, "bold")).grid(column=2, row=x, sticky='W')
        #ttk.Separator(self,orient='horizontal').grid(row=2, columnspan=2, sticky='S')
        x = 2
        for dev_string in port_name:
            tk.Label(self, text=dev_string).grid(column=1, row=x, sticky='W')
            tk.Label(self, text=port_name[dev_string]).grid(column=2, row=x, sticky='W')
            x += 1

        tk.Button(self, text="Open Serial Communicator",
                  command=lambda: master.switch_frame(PageOne)).grid(column=1, row=x, sticky='W')

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.state('zoomed')
        tk.Label(self, text="This is page one").grid(column=1, row=1, sticky='W')
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(Com_viewer)).grid(column=1, row=2, sticky='W')

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.geometry("500x200")
        tk.Label(self, text="This is page two").grid(column=1, row=1, sticky='W')
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(Com_viewer)).grid(column=1, row=2, sticky='W')

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


if __name__ == "__main__":
    list_ports()
    app = SampleApp()
    app.mainloop()
