import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import buttons as but
import json
import serial_functions as SF
import threading
import os

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
top_widgets_list = []
canvas_command_list = []
ascii_command_list = []
transaction_window = []
Listen_mode_send_b = []
Listen_mode_command=[]
interval = []
#frames:
top = []
command = []
trans = []
trans2 = []
options = []
tk_tk = []
startup_flag = 0
serial_flag = 0
listen_mode = False
profile_filename = ""
reason_4_start = 0 # 0=firstboot, 1=change_byte_format, 2=switch_profile






def restart_frame(frame_flag):
    #Flags: top = 0, command = 1, trans = 3, trans2 = 4, options=5
    #clear global list
    if frame_flag == 1: #command frame
        label_CN_list.clear()
        label_byte_list.clear()
        play_but_list.clear()
        canvas_list.clear()
        canvas_command_list.clear()
        command[0].destroy()
        command.pop(0)
        command.append(Commandframe(tk_tk[0]))
    if frame_flag == 5:
        options[0].destroy()
        options.pop(0)
        options.append(Optionsframe(tk_tk[0]))



ascii_flag = 1 #0 = ascii, 1 = hex
#****************************** Add Command Window *********************************************
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.title("Serial Chatter")
        #self.switch_frame(Main_frame)
        self.state('zoomed')
        upper_frame = tk.Frame(self)
        upper_frame.grid(row=0, sticky="news")

        top.append(Topframe(upper_frame))

        lower_frame = tk.Frame(self)
        lower_frame.grid(row=1, sticky="news")

        command.append(Commandframe(lower_frame))
        trans.append(Transactionframe(lower_frame))
        trans2.append(Transactionframe2(lower_frame))
        options.append(Optionsframe(lower_frame))
        tk_tk.append(self)
    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

    def restart_frame(self, frame,tk_tk):
        frame[0].destroy()
        frame.pop(0)
        Commandframe(tk_tk)

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
        tk.Frame.__init__(self, master, borderwidth = 10)
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

    def send_serial_command(self,index): #sending single serial command.
        global unsaved_profile
        global interval
        global ascii_flag
        global listen_mode
        global Listen_mode_command
        if listen_mode == False:
            timeout = float(interval[0].get())
            bytes = unsaved_profile['Commands'][index]['bytes']
            com_port = unsaved_profile['Com Port']
            baudrate = unsaved_profile['Baudrate']
            trans_bytes = ""
            command_n = unsaved_profile['Commands'][index]['name']
            transaction_window[2].insert(tk.END,"********************************************" + "\r\n")
            transaction_window[2].insert(tk.END,"Command: " + command_n + "\r\n")
            if ascii_flag == 1:
                trans_bytes = bytes
            elif ascii_flag == 0:
                trans_bytes = SF.hex_2_ascii(bytes)
            elif ascii_flag == 2:
                trans_bytes = SF.hex_2_dec(bytes)
            transaction_window[2].insert(tk.END,"TX: " + trans_bytes + "\r\n")
            transaction_window[2].update()
            SF.send_serial(bytes,com_port,baudrate,transaction_window[2],timeout,ascii_flag,listen_mode)
        else:
            command_n = unsaved_profile['Commands'][index]['name']
            #transaction_window[2].insert(tk.END,"********************************************" + "\r\n")
            transaction_window[2].insert(tk.END, "\r\n"  + "Command: " + command_n + "\r\n")
            Listen_mode_command.clear()
            Listen_mode_command.append(unsaved_profile['Commands'][index]['bytes'])
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
            global ascii_flag
            global startup_flag
            global reason_4_start
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
                if reason_4_start == 0 or reason_4_start == 2 :
                     unsaved_profile = profile


                if unsaved_profile['Byte Format'] == "ASCII":
                    ascii_flag = 0
                elif unsaved_profile['Byte Format'] == "HEX":
                    ascii_flag = 1
                elif unsaved_profile['Byte Format'] == "DEC":
                    ascii_flag = 2
                #self.update_ascii_commands(unsaved_profile)
                num_commands = len(unsaved_profile['Commands'])
                print("Number of Commands " + str(num_commands) )

                vsb.grid(row=0, column=1, sticky='ns')
                #vsb2 = tk.Scrollbar(frame_canvas, orient="horizontal", command=canvas.xview)
                #vsb2.grid(row=num_commands, column=0, sticky='ew')
                canvas.configure(yscrollcommand=vsb.set)
                for x in range(0,num_commands):
                    B_P = tk.Button(frame_labels, text=">>",command=lambda x=x: self.send_serial_command(x))
                    B_P.grid(column=1, row=x+3, sticky='WNES')
                    play_but_list.append(B_P)
                    name_lenght = len(unsaved_profile['Commands'][x]['name'])
                    if name_lenght > 30:
                        final_name_string = unsaved_profile['Commands'][x]['name'][0:29] + " ..."
                    else:
                        final_name_string = unsaved_profile['Commands'][x]['name']
                    CN = tk.Label(frame_labels, text=final_name_string,borderwidth=1, relief="solid", bg="white",anchor="w")
                    CN.grid(column=2, row=x+3, sticky='WNES')
                    label_CN_list.append(CN)
                bytes_s=""
                for y in range(0,num_commands):
                    print("ascii_flag = ", ascii_flag)
                    if ascii_flag == 1:
                        bytes_s = unsaved_profile['Commands'][y]['bytes']
                    elif ascii_flag == 0:
                        bytes_s = SF.hex_2_ascii(unsaved_profile['Commands'][y]['bytes'])
                    elif ascii_flag == 2:
                        bytes_s = SF.hex_2_dec(unsaved_profile['Commands'][y]['bytes'])
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

    def update_command_list(self,frame,profile,main_frame_canvas,main_canvas,frame_labels,vsb):
        global entry_CN_list
        global entry_byte_list
        global remove_but_list
        global label_CN_list
        global label_byte_list
        global play_but_list
        global ascii_flag
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
            print("ascii_flag = ", ascii_flag)
            if ascii_flag == 1:
                bytes_s = profile['Commands'][y]['bytes']
            elif ascii_flag == 0:
                bytes_s = SF.hex_2_ascii(profile['Commands'][y]['bytes'])
            elif ascii_flag == 2:
                bytes_s = SF.hex_2_dec(profile['Commands'][y]['bytes'])
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
                Ex_ph.bind("<Button-3>", RightClicker)
                entry_CN_list.append(Ex_ph)
                Ey_ph = ttk.Entry(frame_entries,width=80)
                Ey_ph.bind("<Button-3>", RightClicker)
                entry_byte_list.append(Ey_ph)
            for x in range(0,num_commands):
                index = x
                remove_button = ttk.Button(frame_entries, text="-", command =lambda index=index:  self.remove_command(popup,frame_entries,frame_canvas,index,vsb) )
                remove_button.grid(column=1, row=x, sticky='WNES')
                remove_but_list[x] = remove_button
                Ex = ttk.Entry(frame_entries,width=30)
                Ex.bind("<Button-3>", RightClicker)
                Ex.insert(0, unsaved_profile['Commands'][x]['name'])
                Ex.grid(column=2, row=x, sticky='WNES')
                entry_CN_list[x] = Ex
                #bytes_s = unsaved_profile['Commands'][x]['bytes']
                if ascii_flag == 1:
                    bytes_s = unsaved_profile['Commands'][x]['bytes']
                elif ascii_flag == 0:
                    bytes_s = SF.hex_2_ascii(unsaved_profile['Commands'][x]['bytes'])
                elif ascii_flag == 2:
                    bytes_s = SF.hex_2_dec(unsaved_profile['Commands'][x]['bytes'])
                Ey = ttk.Entry(frame_entries,width=80)
                Ey.bind("<Button-3>", RightClicker)
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
            Ex.bind("<Button-3>", RightClicker)
            Ex.insert(0, profile['Commands'][x]['name'])
            Ex.grid(column=2, row=x, sticky='WNES')
            entry_CN_list[x] = Ex
            #bytes_s = profile['Commands'][x]['bytes']
            if ascii_flag == 1:
                bytes_s = unsaved_profile['Commands'][x]['bytes']
            elif ascii_flag == 0:
                bytes_s = SF.hex_2_ascii(unsaved_profile['Commands'][x]['bytes'])
            elif ascii_flag == 2:
                bytes_s = SF.hex_2_dec(unsaved_profile['Commands'][x]['bytes'])
            Ey = ttk.Entry(frame_entries,width=80)
            Ey.bind("<Button-3>", RightClicker)
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
        Ex_ph.bind("<Button-3>", RightClicker)
        entry_CN_list.append(Ex_ph)
        Ey_ph = ttk.Entry(frame_entries,width=30)
        Ey_ph.bind("<Button-3>", RightClicker)
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
            global ascii_flag
            #print("Store Entries")
            print("store_entries " + str(unsaved_profile['Num_Commands']) )
            x=0
            for entry in entry_CN_list:
                unsaved_profile['Commands'][x]['name'] = entry.get()
                x+=1
            y=0
            for entry in entry_byte_list:
                if ascii_flag == 1:
                    unsaved_profile['Commands'][y]['bytes'] = entry.get()
                elif ascii_flag == 0:
                    unsaved_profile['Commands'][y]['bytes'] = SF.ascii_2_hex(entry.get())
                elif ascii_flag == 2:
                    unsaved_profile['Commands'][y]['bytes'] = SF.dec_2_hex(entry.get())
                #unsaved_profile['Commands'][y]['bytes'] = entry.get()
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



class Transactionframe2(tk.Frame):

    def __init__(self, master):
        global Listen_mode_send_b
        tk.Frame.__init__(self, master)
        self.grid(column=1, row=2, sticky=('NSEW'))

        #add label, entry and send button
        send_label = tk.Label(self, text="Send Data Console (Listen Mode Only)")
        send_label.grid(column=0, row=0, sticky='EW')
        input_entry = tk.Entry(self,width=80) #ttk may be needed.
        input_entry.bind("<Button-3>", RightClicker)
        input_entry.grid(column=0, row=1, sticky='EW')
        send_button = ttk.Button(self, text="Send", state="disabled", command =lambda :  self.send_data(input_entry) )
        send_button.grid(column=1, row=1, sticky='W')
        Listen_mode_send_b.append(send_button)

    def send_data(self, entry):
        global ascii_flag
        global Listen_mode_command
        Listen_mode_command.clear()
        command = entry.get()
        if ascii_flag == 1:
            bytes = command
        elif ascii_flag == 0:
            bytes = SF.ascii_2_hex(command)
        elif ascii_flag == 2:
            bytes = SF.dec_2_hex(command)
        print("bytes = " + str(bytes))
        print("command = " + str(command))
        Listen_mode_command.append(bytes)

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
        check_com_match = False
        com_s = unsaved_profile['Com Port']
        for port in unsaved_config['COM List']:
            end_of_com = port.find(":")
            if end_of_com != -1:
                com_match = port[:end_of_com].find(com_s)
                if com_match != -1:
                    check_com_match = True
        if check_com_match:
            COM_v.set(com_s + "  Device Active")
        else:
            COM_v.set(com_s + "  Device Inactive")
        #COM_v.set("COM Port")
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
        baudrate_entry.bind("<Button-3>", RightClicker)

        space2 = tk.Label(self)
        space2.grid(column=1, row=4,sticky='WENS')

        ascii_v = tk.StringVar(self)
        #ascii_v.set("Select Byte Format")
        #set starting value of ascii dropdown to be bootup value from profile
        if ascii_flag == 0:
            ascii_v.set("ASCII")
        elif ascii_flag == 1:
            ascii_v.set("HEX")
        elif ascii_flag == 2:
            ascii_v.set("DEC")
        ascii_array = ["HEX","DEC","ASCII"]
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
        Interval_entry.bind("<Button-3>", RightClicker)
        interval.append(Interval_entry)

    def change_ascii(self,byte_type):
        global command
        global tk_tk
        global label_CN_list
        global label_byte_list
        global play_but_list
        global canvas_list
        global canvas_command_list
        global ascii_flag
        global unsaved_profile
        global reason_4_start
        if(byte_type == "HEX"):
            ascii_flag=1
            unsaved_profile['Byte Format'] = "HEX"
            print("Switching to Hex")
        elif(byte_type == "ASCII"):
            ascii_flag=0
            unsaved_profile['Byte Format'] = "ASCII"
            print("Switching to Ascii")
        elif(byte_type == "DEC"):
            ascii_flag=2
            unsaved_profile['Byte Format'] = "DEC"
            print("Switching to Dec")

        #clear global list
        reason_4_start = 1
        label_CN_list.clear()
        label_byte_list.clear()
        play_but_list.clear()
        canvas_list.clear()
        canvas_command_list.clear()
        command[0].destroy()
        command.pop(0)
        command.append(Commandframe(tk_tk[0]))
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
        COM_drop.config(width=40, font=('Helvetica', 12))
        COM_drop.grid(column=2, row=1, sticky='W')

class Topframe(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, borderwidth = 10) #relief="solid" will make boarder a solid color
        self.grid(column=0, row=0, sticky=('EW'))


        global top_widgets_list
        #Button Ribbon
        # frame_canvas = tk.Frame(self)
        # frame_canvas.grid(row=2, column=1, sticky='nsew')
        # frame_canvas.grid_rowconfigure(0, weight=1)
        # frame_canvas.grid_columnconfigure(0, weight=1)
        # frame_canvas.grid_propagate(False)
        # canvas = tk.Canvas(frame_canvas, bg="yellow")
        # canvas.grid(row=0, column=0, sticky="news")
        # frame_ribbon = tk.Frame(canvas)
        # id= canvas.create_window((0, 0), window=frame_ribbon, anchor='nw')

        #save profile changes
        save_b = tk.Button(self, text="Save", command=lambda : self.temp_save_button() )
        save_b.grid(column=0, row=2, sticky='W')
        top_widgets_list.append(save_b)

        #New profile with current settings
        new_b = tk.Button(self, text="Save As", command=lambda : self.new_profile() )
        new_b.grid(column=1, row=2, sticky='W')
        top_widgets_list.append(new_b)

        #Play List of commands
        play_loop = tk.Button(self, text="Loop", command=lambda : self.loop_through_serial_commands())
        play_loop.grid(column=6, row=2, sticky='W')
        top_widgets_list.append(play_loop)

        #Write transaction log to file
        write_2_log = tk.Button(self, text="Write 2 file",command=lambda : self.write_2_file())
        write_2_log.grid(column=3, row=2, sticky='W')
        top_widgets_list.append(write_2_log)

        #Clear Transaction Terminal
        clear_trans = tk.Button(self, text="Clear Terminal", command=lambda : self.clear_trans())
        clear_trans.grid(column=4, row=2, sticky='W')
        top_widgets_list.append(clear_trans)

        #Start-Stop Listen Mode
        listen_m = tk.Button(self, text="Listen", command=lambda : self.start_stop_serial_thread())
        listen_m.grid(column=5, row=2, sticky='W')
        top_widgets_list.append(listen_m)

        #Switch Profile
        switch_p = tk.Button(self, text='Switch Profile', command=self.switch_profile)
        switch_p.grid(column=2, row=2, sticky='W')
        top_widgets_list.append(switch_p)

        #print profile in use in label
        profile_name =  self.get_profile_name()
        profile_label_text = "|| Active Profile: " + profile_name + " ||"
        my_profile_var = tk.StringVar()
        my_profile_var.set(profile_label_text)
        profile_label = tk.Label(self, textvariable=my_profile_var)
        profile_label.grid(column=7, row=2, sticky='E')
        top_widgets_list.append(profile_label)
        top_widgets_list.append(my_profile_var)

        #label for listen mode
        listen_var = tk.StringVar()
        listen_var.set("                     ")
        listen_label = tk.Label(self, textvariable=listen_var)
        listen_label.grid(column=8, row=2, sticky='E')
        top_widgets_list.append(listen_label)
        top_widgets_list.append(listen_var)



        # frame_ribbon.update_idletasks()
        # columns_width = save_b.winfo_width() + new_b.winfo_width() + play_loop.winfo_width() + write_2_log.winfo_width() + clear_trans.winfo_width() + listen_m.winfo_width() + switch_p.winfo_width() + profile_label.winfo_width() + listen_label.winfo_width()
        # rows_height = save_b.winfo_height()
        #
        # #window_height = remove_but_list[0].winfo_height() * (num_commands)
        # #print("vsb width" + str(vsb.winfo_width()) )
        # frame_canvas.config(width=columns_width, height=rows_height)


        #top_widgets_list index: 0=save, 1=new, 2=play loop, 3=write 2 file, 4=clear log, 5=listen mode, 6=switch profile, 7= profile label, 8=my_profile_var, 9=listen label, 10= listen var

    def write_2_file(self):
        global transaction_window
        contents = transaction_window[2].get("1.0",'end-1c')
        log_file = filedialog.asksaveasfilename(filetypes = [("Text",'*.txt')])
        print(log_file)
        with open(log_file, "w") as write_file:
            write_file.write(contents)
            write_file.close()

    def clear_trans(self):
        global transaction_window
        contents = transaction_window[2].delete("1.0",'end-1c')

    def new_profile(self):
        unsaved_profile
        new_profile = filedialog.asksaveasfilename(filetypes = [("Json",'*.json')], defaultextension = [("Json",'*.json')])
        print(new_profile)
        with open(new_profile, "w") as write_file:
            json.dump(unsaved_profile, write_file, ensure_ascii=False, indent=4)
            write_file.close()
        config = {}
        with open("../json/config.json", "r") as config_file:
            config = json.loads(config_file.read())
            config_file.close()
        config['Profile'] = new_profile
        with open("../json/config.json", "w") as config_file:
            json.dump(config, config_file, ensure_ascii=False, indent=4)
            config_file.close()
        #change label to reflect new profile.
        profile_name =  self.get_profile_name()
        profile_label_text = "|| Active Profile: " + profile_name + " ||"
        top_widgets_list[8].set(profile_label_text) #set label string var to new profile


    def get_profile_name(self):
        with open("../json/config.json", "r") as config_file:
            config = json.loads(config_file.read())
            config_file.close()
        profile_name_w_path = config['Profile']
        return os.path.basename(profile_name_w_path)

    def switch_profile(self):
        global profile_filename
        global top_widgets_list
        global reason_4_start
        #comemented line opens file
        #profile_filename = filedialog.askopenfile(parent=self,mode='rb',title='Choose a file')
        selected_profile = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = [("Json",'*.json')])
        print(selected_profile)
        config = {}
        with open("../json/config.json", "r") as config_file:
            config = json.loads(config_file.read())
            config_file.close()
        config['Profile'] = selected_profile
        with open("../json/config.json", "w") as config_file:
            json.dump(config, config_file, ensure_ascii=False, indent=4)
            config_file.close()
        reason_4_start = 2
        restart_frame(1)
        restart_frame(5)
        #change label to reflect new profile.
        profile_name =  self.get_profile_name()
        profile_label_text = "|| Active Profile: " + profile_name + " ||"
        top_widgets_list[8].set(profile_label_text) #set label string var to new profile

    def temp_save_button(self):
        config = {}
        with open("../json/config.json", "r") as read_file:
            config = json.loads(read_file.read())
            read_file.close()
        with open(config['Profile'], "w") as write_file:
            json.dump(unsaved_profile, write_file, ensure_ascii=False, indent=4)
            write_file.close()

    def start_stop_serial_thread(self):
        global listen_mode
        global Listen_mode_send_b
        global top_widgets_list
        if listen_mode == False:
            top_widgets_list[10].set(" Listen Mode Active ||")
            listen_mode = True
            Listen_mode_send_b[0].config(state="normal")
            t = threading.Thread(target = self.serial_listen)
            t.daemon = True
            t.start()
        else:
            top_widgets_list[10].set("                     ")
            listen_mode = False
            Listen_mode_send_b[0].config(state="disabled")

    def serial_listen(self):
        global tk_tk
        global unsaved_profile
        global serial_flag
        global listen_mode
        global transaction_window
        global ascii_flag
        global Listen_mode_command
        timeout = unsaved_profile['Interval']
        com_port = unsaved_profile['Com Port']
        baudrate = unsaved_profile['Baudrate']
        timeout = 1 #may not need.
        #if in listen mode and serial line isn't begin used read serial
        while listen_mode:

            if len(Listen_mode_command) == 0:
                SF.listener(com_port,baudrate,transaction_window[2],timeout,ascii_flag)
            else:
                trans_bytes = ""
                if ascii_flag == 1:
                    trans_bytes = Listen_mode_command[0]
                elif ascii_flag == 0:
                    trans_bytes = SF.hex_2_ascii(Listen_mode_command[0])
                elif ascii_flag == 2:
                    trans_bytes = SF.hex_2_dec(Listen_mode_command[0])
                transaction_window[2].insert(tk.END,"\r\nTX: " + trans_bytes + "\r\n")
                transaction_window[2].update()
                SF.send_serial(Listen_mode_command[0],com_port,baudrate,transaction_window[2],timeout,ascii_flag,listen_mode)
                Listen_mode_command.clear()
        #Possibly loop though the gui with this

    def loop_through_serial_commands(self): #sending all serial commands.
        global unsaved_profile
        global interval
        global ascii_flag
        global listen_mode
        global transaction_window
        if listen_mode == False:
            timeout = float(interval[0].get())
            unsaved_profile['Interval'] = timeout
            for command in unsaved_profile['Commands']:
                bytes = command['bytes']
                com_port = unsaved_profile['Com Port']
                baudrate = unsaved_profile['Baudrate']
                command_n = command['name']
                transaction_window[2].insert(tk.END,"********************************************" + "\r\n")
                transaction_window[2].insert(tk.END,"Command: " + command_n + "\r\n")
                if ascii_flag == 1:
                    trans_bytes = command['bytes']
                elif ascii_flag == 0:
                    trans_bytes = SF.hex_2_ascii(command['bytes'])
                elif ascii_flag == 2:
                    trans_bytes = SF.hex_2_dec(command['bytes'])
                transaction_window[2].insert(tk.END,"TX: " + trans_bytes + "\r\n")
                transaction_window[2].update()
                SF.send_serial(bytes,com_port,baudrate,transaction_window[2],timeout,ascii_flag,listen_mode)
            print("End of commmand loop.")

class RightClicker: #from: https://stackoverflow.com/questions/57701023/tkinter-notepad-program-trying-to-make-a-right-click-copy-paste-option-really-ne
    def __init__(self, e):
        commands = ["Cut","Copy","Paste"]
        menu = tk.Menu(None, tearoff=0, takefocus=0)

        for txt in commands:
            menu.add_command(label=txt, command=lambda e=e,txt=txt:self.click_command(e,txt))

        menu.tk_popup(e.x_root + 40, e.y_root + 10, entry="0")

    def click_command(self, e, cmd):
        e.widget.event_generate(f'<<{cmd}>>')





class NewWindow(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("New Window")
        master.geometry("200x200")
        tk.Label(self, text ="This is a new Window").grid(column=0, row=0, sticky='W')
