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
canvas_list = []
canvas_command_list = []
ascii_command_list = []
transaction_window = []
interval = []
ascii_flag = 1 #0 = ascii, 1 = hex
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

        frame_canvas = tk.Frame(self)
        frame_canvas.grid(row=3, column=0, pady=(5, 0), sticky='nsew')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        canvas = tk.Canvas(frame_canvas, bg="yellow")
        canvas.grid(row=0, column=0, sticky="news")
        canvas_command_list.append(canvas)
        # Create a frame to contain the buttons
        frame_labels = tk.Frame(canvas)
        id= canvas.create_window((0, 0), window=frame_labels, anchor='nw')
        canvas_command_list.append(id)
        vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        tk.Button(self, text="Edit Command List",command=lambda : self.popupmsg(self,frame_canvas,canvas,frame_labels,vsb)).grid(column=0, row=1, sticky='WN')
        self.list_commands(self,frame_canvas,canvas,frame_labels,vsb)
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
    def send_serial_command(self,index):
        global unsaved_profile
        bytes = unsaved_profile['Commands'][index]['bytes']
        com_port = unsaved_profile['Com Port']
        baudrate = unsaved_profile['Baudrate']
        transaction_window[2].insert(tk.END,"TX: " + str(bytes) + "\r\n")
        transaction_window[2].update()
        SF.send_serial(bytes,com_port,baudrate,transaction_window[2],5)
    def update_ascii_commands(self, profile):
        global ascii_command_list
        ascii_command_list = profile['Commands']
        #print(ascii_command_list)
        name = ""
        bytes = ""
        for x in range(0,profile['Num_Commands']):
            name = ascii_command_list[x]['name']
            print(name)
            ascii_command_list[x]['bytes'] = SF.hex_2_ascii(ascii_command_list[x]['bytes'])
            bytes = ascii_command_list[x]['bytes']
            print(bytes)
    def list_commands(self,frame,frame_canvas,canvas,frame_labels,vsb):
            global entry_CN_list
            global entry_byte_list
            global remove_but_list
            global label_CN_list
            global label_byte_list
            global play_but_list
            global unsaved_profile
            #load config data
            config = {}
            with open("../json/config.json", "r") as read_file:
                config = json.loads(read_file.read())
                read_file.close()
            #print command table
            tk.Label(frame_labels, text="Command Names").grid(column=2, row=2, sticky='WN')
            tk.Label(frame_labels, text="Byte String").grid(column=3, row=2, sticky='WN')
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
                unsaved_profile = profile
                num_commands = len(profile['Commands'])
                print("Number of Commands " + str(num_commands) )

                vsb.grid(row=0, column=1, sticky='ns')
                #vsb2 = tk.Scrollbar(frame_canvas, orient="horizontal", command=canvas.xview)
                #vsb2.grid(row=num_commands, column=0, sticky='ew')
                canvas.configure(yscrollcommand=vsb.set)
                for x in range(0,num_commands):
                    B_P = tk.Button(frame_labels, text=">>",command=lambda x=x: self.send_serial_command(x))
                    B_P.grid(column=1, row=x+3, sticky='WNES')
                    play_but_list.append(B_P)
                    name_lenght = len(profile['Commands'][x]['name'])
                    if name_lenght > 30:
                        final_name_string = profile['Commands'][x]['name'][0:29] + " ..."
                    else:
                        final_name_string = profile['Commands'][x]['name']
                    CN = tk.Label(frame_labels, text=final_name_string,borderwidth=1, relief="solid", bg="white",anchor="w")
                    CN.grid(column=2, row=x+3, sticky='WNES')
                    label_CN_list.append(CN)
                bytes_s=""
                for y in range(0,num_commands):
                    bytes_s = profile['Commands'][y]['bytes']
                    byte_lenght = len(bytes_s)
                    if byte_lenght > 30:
                        final_byte_string = bytes_s[0:29] + " ..."
                    else:
                        final_byte_string = bytes_s
                    CB = tk.Label(frame_labels, text=final_byte_string,borderwidth=1, relief="solid",bg="white",anchor="w")
                    CB.grid(column=3, row=y+3, sticky='WNES')
                    label_byte_list.append(CB)
                    bytes_s=""
                frame_labels.update_idletasks()

                columns_width = label_byte_list[0].winfo_width() + play_but_list[0].winfo_width() + label_CN_list[0].winfo_width()
                if(num_commands <= 15):
                    rows_height = label_byte_list[0].winfo_height() * (num_commands+1)
                else:
                    rows_height = label_byte_list[0].winfo_height() * 16
                print("list_commands columns_width" + str(columns_width))
                print("list_commands rows_height " + str(rows_height))
                frame_canvas.config(width=columns_width + vsb.winfo_width(),height=rows_height)
                canvas.config(scrollregion=canvas.bbox("all"))
            self.update_ascii_commands(unsaved_profile)
    def update_command_list(self,frame,profile,main_frame_canvas,main_canvas,frame_labels,vsb):
        global entry_CN_list
        global entry_byte_list
        global remove_but_list
        global label_CN_list
        global label_byte_list
        global play_but_list
        num_commands = len(profile['Commands'])
        print("update_command_list " + str(num_commands))
        print("update_command_list label_CN_List " + str(len(label_CN_list)))
        # for x in range(0,num_commands):
        #     B_P = tk.Button(frame_labels, text=">>")
        #     play_but_list.append(B_P)
        #     label_CN_list.append(B_P)
        #     label_byte_list.append(B_P)

        for x in range(0,num_commands):
            B_P = tk.Button(frame_labels, text=">>", command=lambda x=x: self.send_serial_command(x))
            B_P.grid(column=1, row=x+3, sticky='WNES')
            play_but_list.append(B_P)
            name_lenght = len(profile['Commands'][x]['name'])
            if name_lenght > 30:
                final_name_string = profile['Commands'][x]['name'][0:29] + " ..."
            else:
                final_name_string = profile['Commands'][x]['name']
            CN = tk.Label(frame_labels, text=final_name_string,borderwidth=1, relief="solid", bg="white",anchor="w")
            print("command name " + str(profile['Commands'][x]['name']))
            CN.grid(column=2, row=x+3, sticky='WNES')
            label_CN_list.append(CN)
        bytes_s=""
        for y in range(0,num_commands):
            bytes_s = profile['Commands'][y]['bytes']
            print("byte string" + bytes_s)
            byte_lenght = len(bytes_s)
            if byte_lenght > 30:
                final_byte_string = bytes_s[0:29] + " ..."
            else:
                final_byte_string = bytes_s
            CB = tk.Label(frame_labels, text=final_byte_string,borderwidth=1, relief="solid",bg="white",anchor="w")
            CB.grid(column=3, row=y+3, sticky='WNES')
            label_byte_list.append(CB)
            bytes_s=""

        frame_labels.update_idletasks()

        columns_width = label_byte_list[0].winfo_width() + play_but_list[0].winfo_width() + label_CN_list[0].winfo_width()
        if(num_commands <= 15):
            rows_height = label_byte_list[0].winfo_height() * (num_commands+1)
        else:
            rows_height = label_byte_list[0].winfo_height() * 16
        window_height = remove_but_list[0].winfo_height() * (num_commands)
        print("update_command_list columns_width" + str(columns_width))
        print("update_command_list rows_height" + str(rows_height))
        main_frame_canvas.config(width=columns_width + vsb.winfo_width(),height=rows_height)
        #main_canvas.itemconfig(canvas_command_list[1],height=window_height)
        main_canvas.config(scrollregion=main_canvas.bbox("all"))
        self.update_ascii_commands(profile)

    def popupmsg(self,frame,main_frame_canvas,main_canvas,frame_labels,main_vsb):
        global entry_CN_list
        global entry_byte_list
        global remove_but_list
        global label_CN_list
        global label_byte_list
        global play_but_list
        global unsaved_profile
        #clear data from previous iterations

        remove_but_list*= 0
        entry_CN_list*= 0
        entry_byte_list*= 0


        popup = tk.Tk()
        popup.title("!")
        profile = {}
        num_commands=0
        w = 800
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
        apply_b = ttk.Button(popup, text="Apply", command =lambda :  self.store_entries(frame,main_frame_canvas,main_canvas,frame_labels,main_vsb) ).grid(column=1, row=1, sticky='WNS')

        frame_canvas = tk.Frame(popup)
        frame_canvas.grid(row=2, column=1, pady=(5, 0), sticky='nw')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        canvas = tk.Canvas(frame_canvas, bg="yellow")
        canvas.grid(row=0, column=0, sticky="news")
        canvas_list.append(canvas)
        # Create a frame to contain the buttons
        frame_entries = tk.Frame(canvas)
        id = canvas.create_window((0, 0), window=frame_entries, anchor='nw')
        canvas_list.append(id)

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
            if not bool(unsaved_profile):
                with open(config_p['Profile'], "r") as read_file:
                    profile = json.loads(read_file.read())
                    unsaved_profile=profile.copy()
                    #print("num commands = %d",unsaved_profile['Num_Commands'])
                    read_file.close()
                num_commands = len(profile['Commands'])
            else:
                num_commands = len(unsaved_profile['Commands'])

            # Link a scrollbar to the canvas
            vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
            vsb.grid(row=0, column=1, sticky='ns')
            #vsb2 = tk.Scrollbar(frame_canvas, orient="horizontal", command=canvas.xview)
            #vsb2.grid(row=num_commands, column=0, sticky='ew')
            canvas.configure(yscrollcommand=vsb.set)
            add_button = ttk.Button(popup, text="+", command =lambda : self.add_command(popup,frame_entries,frame_canvas,vsb))
            add_button.grid(column=1, row=3, sticky='WNES')
            for w in range (0,num_commands):
                remove_button_ph = ttk.Button(frame_entries)
                remove_but_list.append(remove_button_ph)
                Ex_ph = ttk.Entry(frame_entries,width=30)
                entry_CN_list.append(Ex_ph)
                Ey_ph = ttk.Entry(frame_entries,width=80)
                entry_byte_list.append(Ey_ph)
            for x in range(0,num_commands):
                index = x
                remove_button = ttk.Button(frame_entries, text="-", command =lambda index=index:  self.remove_command(popup,frame_entries,frame_canvas,index,vsb) )
                remove_button.grid(column=1, row=x, sticky='WNES')
                remove_but_list[x] = remove_button
                Ex = ttk.Entry(frame_entries,width=30)
                Ex.insert(0, unsaved_profile['Commands'][x]['name'])
                Ex.grid(column=2, row=x, sticky='WNES')
                entry_CN_list[x] = Ex
                bytes_s = unsaved_profile['Commands'][x]['bytes']
                Ey = ttk.Entry(frame_entries,width=80)
                Ey.insert(0, bytes_s)
                Ey.grid(column=3, row=x, sticky='WNES')
                entry_byte_list[x] = Ey
        frame_entries.update_idletasks()

        columns_width = remove_but_list[0].winfo_width() + entry_CN_list[0].winfo_width() +  entry_byte_list[0].winfo_width()
        if(num_commands <= 15):
            rows_height = remove_but_list[0].winfo_height() * (num_commands)
        else:
            rows_height = remove_but_list[0].winfo_height() * 16
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
        print("update_command_entries "+str(len(remove_but_list)) )
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
            Ey = ttk.Entry(frame_entries,width=80)
            Ey.insert(0, bytes_s)
            Ey.grid(column=3, row=x, sticky='WNES')
            entry_byte_list[x] = Ey
        frame_entries.update_idletasks()

        columns_width = remove_but_list[0].winfo_width() + entry_CN_list[0].winfo_width() +  entry_byte_list[0].winfo_width()
        if(num_commands <= 15):
            rows_height = remove_but_list[0].winfo_height() * (num_commands)
        else:
            rows_height = remove_but_list[0].winfo_height() * 16
        window_height = remove_but_list[0].winfo_height() * (num_commands)
        frame_canvas.config(width=columns_width + vsb.winfo_width(),height=rows_height)
        canvas_list[0].itemconfig(canvas_list[1],height=window_height)
        canvas_list[0].configure(scrollregion=canvas_list[0].bbox("all"))

    def remove_command(self,popup,frame_entries,frame_canvas,index,vsb):
        global entry_CN_list
        global entry_byte_list
        global remove_but_list
        global label_CN_list
        global label_byte_list
        global play_but_list
        #See if command being deleted is in the current profile.
        # with open("../json/config.json", "r") as read_file:
        #     config_p = json.loads(read_file.read())
        #     read_file.close()
        # if config_p['Profile'] != "../json/default.json":
        #     with open(config_p['Profile'], "r") as read_file:
        #         profile = json.loads(read_file.read())
        #         read_file.close()
        #     num_commands = len(profile['Commands'])
        #     if(index < num_commands): #command is in current profile
        #         profile['Commands'].pop(index)
        #         profile['Num_Commands'] = num_commands-1


        #print(profile['Commands'])
        #See if command is being deleted is in the unsaved profile
        num_commands = len(unsaved_profile['Commands'])
        #if(index < num_commands): #command is in current profile
        print("remove_command" + str(index))
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
        remove_but_list.pop(index)
        entry_CN_list.pop(index)
        entry_byte_list.pop(index)
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



    def store_entries(self,frame,main_frame_canvas,main_canvas,frame_labels,main_vsb):
            global entry_CN_list
            global entry_byte_list
            global remove_but_list
            global label_CN_list
            global label_byte_list
            global play_but_list
            global unsaved_profile
            #print("Store Entries")
            print("store_entries " + str(unsaved_profile['Num_Commands']) )
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
            self.update_command_list(frame,unsaved_profile,main_frame_canvas,main_canvas,frame_labels,main_vsb)
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
        global transaction_window
        tk.Frame.__init__(self, master)
        self.grid(column=1, row=1, sticky=('NSEW'))

        #transaction_window: 0-canvas, 1-canvas, id 2-text widget

        tk.Label(self, text="Serial Transaction Log").grid(column=1, row=1, sticky='W')


        frame_canvas = tk.Frame(self)
        frame_canvas.grid(row=2, column=1, sticky='nsew')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        canvas = tk.Canvas(frame_canvas, bg="yellow")
        canvas.grid(row=0, column=0, sticky="news")
        transaction_window.append(canvas)
        # Create a frame to contain the buttons
        frame_text = tk.Frame(canvas)
        id= canvas.create_window((0, 0), window=frame_text, anchor='nw')
        transaction_window.append(id)
        vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)

        vsb.grid(row=0, column=1, sticky='ns')
        #canvas.configure(yscrollcommand=vsb.set)

        text_w = tk.Text(frame_text)
        text_w.grid(column=1, row=1, sticky='NSEW')
        text_w.configure(yscrollcommand=vsb.set)
        #text_w.insert(tk.END,"Test")
        transaction_window.append(text_w)
        #text_w.insert(tk.END,"Test2")

        frame_text.update_idletasks()

        columns_width = text_w.winfo_width()

        rows_height = text_w.winfo_height()

        #window_height = remove_but_list[0].winfo_height() * (num_commands)
        print("vsb width" + str(vsb.winfo_width()) )
        frame_canvas.config(width=columns_width + vsb.winfo_width(),height=rows_height)
        #main_canvas.itemconfig(canvas_command_list[1],height=window_height)
        canvas.config(scrollregion=canvas.bbox("all"))

class Optionsframe(tk.Frame):

    def __init__(self, master):
        global unsaved_config
        global unsaved_profile
        global interval
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
        com_label = tk.Label(self, text="Serial Device: ")
        com_label.grid(column=1, row=1, sticky='EW')
        COM_drop = tk.OptionMenu(self, COM_v, *unsaved_config['COM List'],command=self.get_com)
        COM_drop.config(width=40, font=('Helvetica', 12))
        COM_drop.grid(column=2, row=1, sticky='W')
        #Setup Com Port Refresh button
        refresh = tk.Button(self, text="Refesh",command=lambda config=config: self.check_COMs(self,COM_drop,COM_v))
        refresh.grid(column=3, row=1, sticky='E')

        space = tk.Label(self)
        space.grid(column=1, row=2,sticky='WENS')

        baud_label = tk.Label(self, text="Baud Rate: ")
        baud_label.grid(column=1, row=3, sticky='EW')
        baudrate = unsaved_profile["Baudrate"]
        baudrate_entry = ttk.Entry(self)
        baudrate_entry.insert(0, baudrate)
        baudrate_entry.grid(column=2, row=3, sticky='WE')

        space2 = tk.Label(self)
        space2.grid(column=1, row=4,sticky='WENS')

        ascii_v = tk.StringVar(self)
        ascii_v.set("Select Byte Format")

        ascii_array = ["HEX","ASCII"]
        ascii_label = tk.Label(self, text="Byte Format: ")
        ascii_label.grid(column=1, row=5, sticky='EW')
        ascii_drop = tk.OptionMenu(self,ascii_v, *ascii_array,command=self.change_ascii)
        ascii_drop.config(width=40, font=('Helvetica', 12))
        ascii_drop.grid(column=2, row=5, sticky='W')

        space3 = tk.Label(self)
        space3.grid(column=1, row=6,sticky='WENS')

        Interval_label = tk.Label(self, text="Time Interval: ")
        Interval_label.grid(column=1, row=7, sticky='EW')
        Interval = unsaved_profile["Interval"]
        Interval_entry = ttk.Entry(self)
        Interval_entry.insert(0, Interval)
        Interval_entry.grid(column=2, row=7, sticky='WE')
        interval.append(Interval_entry)
    def change_ascii(self,byte_type):

        if(byte_type == "HEX"):
            ascii_flag=1;
            print("Switching to Hex")
        elif(byte_type == "ASCII"):
            ascii_flag=0;
            print("Switching to Ascii")
        #print("Test ascii dropdown")
    def get_com(self, value):
        global unsaved_profile
        print("get com has executed")
        print("value = "+value)
        value_index = value.find(":")
        if(value_index == -1):
            print('No COM Port Devices found.')
        else:
            unsaved_profile['Com Port'] = value[:value_index]
            print("unsaved_profile com port = " + unsaved_profile['Com Port'])
    def check_COMs(self,frame,COM_drop,COM_v):
        global unsaved_config
        SF.list_ports()
        with open("../json/config.json", "r") as read_file:
            unsaved_config = json.loads(read_file.read())
            read_file.close()
        COM_drop.grid_forget()
        COM_drop = tk.OptionMenu(frame, COM_v, *unsaved_config['COM List'])
        COM_drop.config(width=90, font=('Helvetica', 12))
        COM_drop.grid(column=2, row=1, sticky='W')

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
                  command=lambda : self.loop_through_serial_commands()).grid(column=2, row=2, sticky='W')
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

    def loop_through_serial_commands(self):
        global unsaved_profile
        global interval
        timeout = float(interval[0].get())
        unsaved_profile['Interval'] = timeout
        for command in unsaved_profile['Commands']:
            bytes = command['bytes']
            com_port = unsaved_profile['Com Port']
            baudrate = unsaved_profile['Baudrate']
            command_n = command['name']
            transaction_window[2].insert(tk.END,"********************************************" + "\r\n")
            transaction_window[2].insert(tk.END,"Command: " + command_n + "\r\n")
            transaction_window[2].insert(tk.END,"TX: " + str(bytes) + "\r\n")
            transaction_window[2].update()
            SF.send_serial(bytes,com_port,baudrate,transaction_window[2],timeout)
        print("End of commmand loop.")

#****************************** Add Command Window *********************************************
class NewWindow(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("New Window")
        master.geometry("200x200")
        tk.Label(self, text ="This is a new Window").grid(column=0, row=0, sticky='W')
