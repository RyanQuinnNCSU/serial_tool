import tkinter as tk
from tkinter import ttk
import buttons as but
import json

filename = "../json/config.json"

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.title("Serial Chatter")
        #self.switch_frame(Main_frame)
        top = Topframe(self)
        test = Commandframe(self)
        trans = Transactionframe(self)
        options = Optionsframe(self)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class Testframe(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)
        self.grid(column=0, row=1, sticky=('NSEW'))
        tk.Label(master, text ="Frame Test").grid(column=1, row=1, sticky='W')


class Commandframe(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)
        self.grid(column=0, row=1, sticky=('WN'))
        #ttk.Separator(self,orient="vertical").grid(column=3, rowspan=3,ipady=300)
        tk.Button(self, text="Edit Command List").grid(column=1, row=1, sticky='WN')
        tk.Label(self, text="Command Names").grid(column=1, row=2, sticky='WN')
        tk.Label(self, text="Byte String").grid(column=2, row=2, sticky='WNN')


class Transactionframe(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)
        self.grid(column=1, row=1, sticky=('NSEW'))
        tk.Label(self, text="Serial Transaction Log").grid(column=1, row=2, sticky='W')
        text_w = tk.Text(self)
        text_w.grid(column=1, row=2, sticky='NSEW')
        text_w.insert(tk.END,"Test")
        #text_w.insert(tk.END,"Test2")

class Optionsframe(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid(column=2, row=1, sticky=('NSEW'))
        config = {}
        with open("../json/config.json", "r") as read_file:
            config = json.loads(read_file.read())
            read_file.close()
        COM_v = tk.StringVar(self)
        COM_v.set("COM Port")
        COM_drop = tk.OptionMenu(self, COM_v, *config['COM List'])
        COM_drop.config(width=90, font=('Helvetica', 12))
        COM_drop.grid(column=1, row=1, sticky='W')

class Topframe(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, borderwidth = 10) #relief="solid" will make boarder a solid color
        self.grid(column=0, row=0, sticky=('EW'))
        master.state('zoomed')
        #Button Ribbon
        tk.Button(self, text="Play Script",
                  command=but.play_button).grid(column=1, row=2, sticky='W')
        tk.Button(self, text="Loop",
                  command=but.loop_button).grid(column=2, row=2, sticky='W')
        tk.Button(self, text="Write 2 file",
                  command=but.write_button).grid(column=3, row=2, sticky='W')
        tk.Button(self, text="Clear Terminal",
                  command=but.clear_button).grid(column=4, row=2, sticky='W')
        #Command table
        # tk.Label(self, text="Command Names").grid(column=2, row=3, sticky='W')
        # tk.Label(self, text="Byte String").grid(column=3, row=3, sticky='W')
        # tk.Button(self, text="Add Name",
        #           command=lambda: master.switch_frame(Testwindow)).grid(column=2, row=4, sticky='W')
        # tk.Button(self, text="Add Bytes",
        #           command=lambda: master.switch_frame(Testwindow)).grid(column=3, row=4, sticky='W')
