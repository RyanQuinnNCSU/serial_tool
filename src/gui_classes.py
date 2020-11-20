import tkinter as tk
from tkinter import ttk
import buttons as but
import json

filename = "../json/config.json"
#****************************** Add Command Window *********************************************
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
        tk.Button(self, text="Edit Command List",command=lambda : self.popupmsg()).grid(column=2, row=1, sticky='WN')
        tk.Label(self, text="Command Names").grid(column=2, row=2, sticky='WN')
        tk.Label(self, text="Byte String").grid(column=3, row=2, sticky='WNN')
        #load config data
        config = {}
        with open("../json/config.json", "r") as read_file:
            config = json.loads(read_file.read())
            read_file.close()
        #print command table
        if config['Profile'] == "../json/default.json":
            #make empty Table
            for x in range(0, 8):
                tk.Button(self, text=">>").grid(column=1, row=x+3, sticky='WNES')
                tk.Label(self, text="       ",borderwidth=1, relief="solid", bg="white").grid(column=2, row=x+3, sticky='WNES')
                tk.Label(self, text="       ",borderwidth=1, relief="solid",bg="white").grid(column=3, row=x+3, sticky='WNES')
        else:
            with open(config['Profile'], "r") as read_file:
                profile = json.loads(read_file.read())
                read_file.close()
            num_commands = len(profile['Commands'])
            for x in range(0,num_commands):

                tk.Button(self, text=">>").grid(column=1, row=x+3, sticky='WNES')
                tk.Label(self, text=profile['Commands'][x]['name'],borderwidth=1, relief="solid", bg="white").grid(column=2, row=x+3, sticky='WNES')
                num_bytes = len(profile['Commands'][x]['bytes'])
                bytes_s=""
                for y in range(0,num_bytes):
                    bytes_s += str(profile['Commands'][x]['bytes'][y]) + " "
                tk.Label(self, text=bytes_s,borderwidth=1, relief="solid",bg="white").grid(column=3, row=x+3, sticky='WNES')
    # def popupmsg(self):
    #         popup = tk.Tk()
    #         popup.wm_title("!")
    #         label = ttk.Label(popup, text="Test", font="NORM_FONT")
    #         label.grid(column=1, row=1, sticky='WNES')
    #         B1 = ttk.Button(popup, text="Okay", command =popup.destroy))
    #         B2 = ttk.Button(popup, text="Okay", command = popup.destroy)
    #         B1.grid(column=1, row=2, sticky='WNES')
    #         B2.grid(column=2, row=2, sticky='WNES')
    #         popup.mainloop()
    def popupmsg(self):
        popup = tk.Tk()
        popup.title("!")
        w = 500
        h = 500
        ws = popup.winfo_screenwidth() # width of the screen
        hs = popup.winfo_screenheight() # height of the screen
        popup.geometry("%dx%d+%d+%d" % (w,h,ws-3*ws/4,hs-3*hs/4))
        # label = ttk.Label(popup, text="Test", font="NORM_FONT")
        # label.grid(column=1, row=1, sticky='WNES')
        # scrollbar = ttk.Scrollbar(popup,orient=tk.HORIZONTAL)
        # scrollbar.grid(column=1, row=3, sticky='WNES')
        # name_var= tk.StringVar()
        # E1 = ttk.Entry(popup,textvariable=name_var)
        # E1.grid(column=1, row=2, sticky='WNES')
        # B1 = ttk.Button(popup, text="print",command=lambda : but.printcheck(E1.get()) ).grid(column=1, row=4, sticky='WNES')
        B2 = ttk.Button(popup, text="Apply", command = popup.destroy).grid(column=2, row=1, sticky='WNES')

        config_p = {}
        with open("../json/config.json", "r") as read_file:
            config_p = json.loads(read_file.read())
            read_file.close()
        #print command table
        if config_p['Profile'] == "../json/default.json":
            #make empty Table
            for x in range(0, 8):
                print(PH)
        else:
            with open(config_p['Profile'], "r") as read_file:
                profile = json.loads(read_file.read())
                read_file.close()
            num_commands = len(profile['Commands'])
            for x in range(0,num_commands):
                Ex = ttk.Entry(popup)
                Ex.insert(0, profile['Commands'][x]['name'])
                Ex.grid(column=1, row=x+1, sticky='WNES')
                num_bytes = len(profile['Commands'][x]['bytes'])
                bytes_s=""
                for y in range(0,num_bytes):
                    bytes_s += str(profile['Commands'][x]['bytes'][y]) + " "
                Ey = ttk.Entry(popup)
                Ey.insert(0, bytes_s)
                Ey.grid(column=2, row=x+1, sticky='WNES')
        popup.mainloop()
    # def table(total_rows, total_columns,self,master,profile):
    #     with open(profile, "r") as profile_file:
    #         profile = json.loads(profile_file.read())
    #         read_file.close()
    #     for i in range(total_rows):
    #         for j in range(total_columns):
    #
    #             self.e = Entry(master, width=20, fg='blue',
    #                            font=('Arial',16,'bold'))
    #
    #             self.e.grid(row=i, column=j)
    #             self.e.insert(END, lst[i][j])
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
        #load config data
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

#****************************** Add Command Window *********************************************
class NewWindow(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("New Window")
        master.geometry("200x200")
        tk.Label(self, text ="This is a new Window").grid(column=0, row=0, sticky='W')
