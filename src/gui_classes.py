import tkinter as tk
from tkinter import ttk
import buttons as but
import json
import serial_functions as SF

filename = "../json/config.json"
unsaved_profile={}
unsaved_config={}
entry_CN_list = []
entry_byte_list = []
remove_but_list = []
label_CN_list = []
label_byte_list = []
play_but_list = []
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
        tk.Button(self, text="Edit Command List",command=lambda : self.popupmsg(self)).grid(column=2, row=1, sticky='WN')
        tk.Label(self, text="Command Names").grid(column=2, row=2, sticky='WN')
        tk.Label(self, text="Byte String").grid(column=3, row=2, sticky='WNN')
        self.list_commands(self)
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
    def list_commands(self,frame):
            global entry_CN_list
            global entry_byte_list
            global remove_but_list
            global label_CN_list
            global label_byte_list
            global play_but_list
            #load config data
            config = {}
            with open("../json/config.json", "r") as read_file:
                config = json.loads(read_file.read())
                read_file.close()
            #print command table
            if config['Profile'] == "../json/default.json":
                #make empty Table
                for x in range(0, 8):
                    tk.Button(frame, text=">>").grid(column=1, row=x+3, sticky='WNES')
                    tk.Label(frame, text="       ",borderwidth=1, relief="solid", bg="white").grid(column=2, row=x+3, sticky='WNES')
                    tk.Label(frame, text="       ",borderwidth=1, relief="solid",bg="white").grid(column=3, row=x+3, sticky='WNES')
            else:
                with open(config['Profile'], "r") as read_file:
                    profile = json.loads(read_file.read())
                    read_file.close()
                num_commands = len(profile['Commands'])
                for x in range(0,num_commands):
                    B_P = tk.Button(frame, text=">>")
                    B_P.grid(column=1, row=x+3, sticky='WNES')
                    play_but_list.append(B_P)
                    CN = tk.Label(frame, text=profile['Commands'][x]['name'],borderwidth=1, relief="solid", bg="white")
                    CN.grid(column=2, row=x+3, sticky='WNES')
                    label_CN_list.append(CN)
                bytes_s=""
                for y in range(0,num_commands):
                    bytes_s = profile['Commands'][y]['bytes']
                    CB = tk.Label(frame, text=bytes_s,borderwidth=1, relief="solid",bg="white")
                    CB.grid(column=3, row=y+3, sticky='WNES')
                    label_byte_list.append(CB)
                    bytes_s=""

    def update_command_list(self,frame,profile):
        global entry_CN_list
        global entry_byte_list
        global remove_but_list
        global label_CN_list
        global label_byte_list
        global play_but_list
        num_commands = len(profile['Commands'])
        for x in range(0,num_commands):
            B_P = tk.Button(frame, text=">>")
            B_P.grid(column=1, row=x+3, sticky='WNES')
            play_but_list.append(B_P)
            CN = tk.Label(frame, text=profile['Commands'][x]['name'],borderwidth=1, relief="solid", bg="white")
            CN.grid(column=2, row=x+3, sticky='WNES')
            label_CN_list.append(CN)
        bytes_s=""
        for y in range(0,num_commands):
            bytes_s = profile['Commands'][y]['bytes']
            CB = tk.Label(frame, text=bytes_s,borderwidth=1, relief="solid",bg="white")
            CB.grid(column=3, row=y+3, sticky='WNES')
            label_byte_list.append(CB)
            bytes_s=""

    def popupmsg(self,frame):
        global entry_CN_list
        global entry_byte_list
        global remove_but_list
        global label_CN_list
        global label_byte_list
        global play_but_list
        global unsaved_profile
        popup = tk.Tk()
        popup.title("!")
        profile = {}
        num_commands=0
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
        apply_b = ttk.Button(popup, text="Apply", command =lambda :  self.store_entries(frame) ).grid(column=1, row=1, sticky='WNS')

        frame_canvas = tk.Frame(popup)
        frame_canvas.grid(row=2, column=1, pady=(5, 0), sticky='nw')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        canvas = tk.Canvas(frame_canvas, bg="yellow")
        canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        # Create a frame to contain the buttons
        frame_entries = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_entries, anchor='nw')

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
                unsaved_profile=profile.copy()
                #print("num commands = %d",unsaved_profile['Num_Commands'])
                read_file.close()
            num_commands = len(profile['Commands'])
            add_button = ttk.Button(popup, text="+", command =lambda : self.add_command(popup,frame_entries,frame_canvas,vsb))
            add_button.grid(column=1, row=3, sticky='WNES')
            for w in range (0,num_commands):
                remove_button_ph = ttk.Button(frame_entries)
                remove_but_list.append(remove_button_ph)
                Ex_ph = ttk.Entry(frame_entries,width=30)
                entry_CN_list.append(Ex_ph)
                Ey_ph = ttk.Entry(frame_entries,width=30)
                entry_byte_list.append(Ey_ph)
            for x in range(0,num_commands):
                index = x
                remove_button = ttk.Button(frame_entries, text="-", command =lambda index=index:  self.remove_command(popup,frame_entries,frame_canvas,index,vsb) )
                remove_button.grid(column=1, row=x, sticky='WNES')
                remove_but_list[x] = remove_button
                Ex = ttk.Entry(frame_entries,width=30)
                Ex.insert(0, profile['Commands'][x]['name'])
                Ex.grid(column=2, row=x, sticky='WNES')
                entry_CN_list[x] = Ex
                bytes_s = profile['Commands'][x]['bytes']
                Ey = ttk.Entry(frame_entries,width=30)
                Ey.insert(0, bytes_s)
                Ey.grid(column=3, row=x, sticky='WNES')
                entry_byte_list[x] = Ey
        frame_entries.update_idletasks()

        columns_width = remove_but_list[0].winfo_width() + entry_CN_list[0].winfo_width() +  entry_byte_list[0].winfo_width()
        rows_height = remove_but_list[0].winfo_height() * num_commands
        frame_canvas.config(width=columns_width + vsb.winfo_width(),height=rows_height)
        # Set the canvas scrolling region



        canvas.config(scrollregion=canvas.bbox("all"))


        popup.mainloop()

    def update_command_entries(self,popup,frame_entries,frame_canvas,vsb,profile):
        global entry_CN_list
        global entry_byte_list
        global remove_but_list
        global label_CN_list
        global label_byte_list
        global play_but_list
        print(len(remove_but_list))
        num_commands = len(profile['Commands'])
        for x in range(0,num_commands):
            index = x
            remove_button = ttk.Button(frame_entries, text="-", command =lambda index=index:  self.remove_command(popup,frame_entries,frame_canvas,index,vsb) )
            remove_button.grid(column=1, row=x, sticky='WNES')
            remove_but_list[x] = remove_button
            Ex = ttk.Entry(frame_entries,width=30)
            Ex.insert(0, profile['Commands'][x]['name'])
            Ex.grid(column=2, row=x, sticky='WNES')
            entry_CN_list[x] = Ex
            bytes_s = profile['Commands'][x]['bytes']
            Ey = ttk.Entry(frame_entries,width=30)
            Ey.insert(0, bytes_s)
            Ey.grid(column=3, row=x, sticky='WNES')
            entry_byte_list[x] = Ey
        frame_entries.update_idletasks()

        columns_width = remove_but_list[0].winfo_width() + entry_CN_list[0].winfo_width() +  entry_byte_list[0].winfo_width()
        rows_height = remove_but_list[0].winfo_height() * num_commands
        frame_canvas.config(width=columns_width + vsb.winfo_width(),height=rows_height)

    def remove_command(self,popup,frame_entries,frame_canvas,index,vsb):
        global entry_CN_list
        global entry_byte_list
        global remove_but_list
        global label_CN_list
        global label_byte_list
        global play_but_list
        #See if command being deleted is in the current profile.
        with open("../json/config.json", "r") as read_file:
            config_p = json.loads(read_file.read())
            read_file.close()
        if config_p['Profile'] != "../json/default.json":
            with open(config_p['Profile'], "r") as read_file:
                profile = json.loads(read_file.read())
                read_file.close()
            num_commands = len(profile['Commands'])
            if(index < num_commands): #command is in current profile
                profile['Commands'].pop(index)
                profile['Num_Commands'] = num_commands-1
        #print(profile['Commands'])
        #See if command is being deleted is in the unsaved profile
        num_commands = len(unsaved_profile['Commands'])
        if(index < num_commands): #command is in current profile
            unsaved_profile['Commands'].pop(index)
            unsaved_profile['Num_Commands'] = num_commands-1
            #print(unsaved_profile['Commands'])
        #remove command widgets
        for x in range(0,len(remove_but_list)):
            remove_but_list[x].grid_forget()
            entry_CN_list[x].grid_forget()
            entry_byte_list[x].grid_forget()
        ##clear widget list
        #remove_but_list *= 0
        #entry_CN_list*= 0
        #entry_byte_list*= 0
        #reset command widgets
        self.update_command_entries(popup,frame_entries,frame_canvas,vsb,unsaved_profile)

    def add_command(self, popup,frame_entries,frame_canvas,vsb):
        global entry_CN_list
        global entry_byte_list
        global remove_but_list
        global label_CN_list
        global label_byte_list
        global play_but_list
        global unsaved_profile
        unsaved_profile['Num_Commands']= unsaved_profile['Num_Commands'] + 1
        # num_commands = unsaved_profile['Num_Commands']
        # remove_button = ttk.Button(frame_entries, text="-", command =lambda :  self.remove_command(popup,num_commands+1,add_button) )
        # remove_button.grid(column=1, row=num_commands+1, sticky='WNES')
        # remove_but_list.append(remove_button)
        # Ex = ttk.Entry(frame_entries)
        # Ex.grid(column=2, row=num_commands, sticky='WNES')
        # entry_CN_list.append(Ex)
        # Ey = ttk.Entry(frame_entries)
        # Ey.grid(column=3, row=num_commands, sticky='WNES')
        # add_button.grid(column=1, row=num_commands+2, sticky='WNES')
        # entry_byte_list.append(Ey)
        #append to global button and entry list_ports
        remove_button_ph = ttk.Button(frame_entries)
        remove_but_list.append(remove_button_ph)
        Ex_ph = ttk.Entry(frame_entries,width=30)
        entry_CN_list.append(Ex_ph)
        Ey_ph = ttk.Entry(frame_entries,width=30)
        entry_byte_list.append(Ey_ph)
        empty_command = { "name":"", "bytes": ""}
        unsaved_profile['Commands'].append(empty_command)
        self.update_command_entries(popup,frame_entries,frame_canvas,vsb,unsaved_profile)



    def store_entries(self,frame):
            global entry_CN_list
            global entry_byte_list
            global remove_but_list
            global label_CN_list
            global label_byte_list
            global play_but_list
            global unsaved_profile
            print("Store Entries")
            x=0
            for entry in entry_CN_list:
                unsaved_profile['Commands'][x]['name'] = entry.get()
                x+=1
            y=0
            for entry in entry_byte_list:
                unsaved_profile['Commands'][y]['bytes'] = entry.get()
                y+=1
            #Update main window.
            for x in range(0,len(play_but_list)):
                play_but_list[x].grid_forget()
                label_CN_list[x].grid_forget()
                label_byte_list[x].grid_forget()
            play_but_list*= 0
            label_CN_list*= 0
            label_byte_list*= 0
            self.update_command_list(frame,unsaved_profile)
            #print(unsaved_profile)
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
        global unsaved_config
        tk.Frame.__init__(self, master)
        self.grid(column=2, row=1, sticky=('NSEW'))
        #load config data
        config = {}
        with open("../json/config.json", "r") as read_file:
            config = json.loads(read_file.read())
            read_file.close()
        unsaved_config = config
        COM_v = tk.StringVar(self)
        COM_v.set("COM Port")
        #Setup Com Port Drop Down Menu.
        COM_drop = tk.OptionMenu(self, COM_v, *unsaved_config['COM List'])
        COM_drop.config(width=90, font=('Helvetica', 12))
        COM_drop.grid(column=1, row=1, sticky='W')
        #Setup Com Port Refresh button
        refresh = tk.Button(self, text="Refesh",command=lambda config=config: self.check_COMs(self,COM_drop,COM_v))
        refresh.grid(column=2, row=1, sticky='E')

    def check_COMs(self,frame,COM_drop,COM_v):
        global unsaved_config
        SF.list_ports()
        with open("../json/config.json", "r") as read_file:
            unsaved_config = json.loads(read_file.read())
            read_file.close()
        COM_drop.grid_forget()
        COM_drop = tk.OptionMenu(frame, COM_v, *unsaved_config['COM List'])
        COM_drop.config(width=90, font=('Helvetica', 12))
        COM_drop.grid(column=1, row=1, sticky='W')

class Topframe(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, borderwidth = 10) #relief="solid" will make boarder a solid color
        self.grid(column=0, row=0, sticky=('EW'))
        master.state('zoomed')
        #Button Ribbon
        tk.Button(self, text="TMP Save",
                  command=lambda : self.temp_save_button() ).grid(column=1, row=1, sticky='W')

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
    def temp_save_button(self):
        config = {}
        with open("../json/config.json", "r") as read_file:
            config = json.loads(read_file.read())
            read_file.close()
        with open(config['Profile'], "w") as write_file:
            json.dump(unsaved_profile, write_file, ensure_ascii=False, indent=4)
            write_file.close()


#****************************** Add Command Window *********************************************
class NewWindow(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("New Window")
        master.geometry("200x200")
        tk.Label(self, text ="This is a new Window").grid(column=0, row=0, sticky='W')
