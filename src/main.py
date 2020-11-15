import tkinter as tk
from tkinter import ttk
# import serial
# from serial.tools import list_ports
import serial_functions as SF
import gui_classes as GUI





if __name__ == "__main__":
    SF.list_ports()
    app = GUI.SampleApp()
    app.mainloop()
