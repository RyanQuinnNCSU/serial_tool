import sys
import serial
import tkinter as tk
from serial.tools import list_ports
import gui_classes
import codecs
import json

config = {}

# ascii_chart = {
# 0: "<NULL>", 1:"<Start of Heading>", 2:"<Start of Text>", 3:"<End of Text>", 4:"<End of Trans>", 5:"<Enquiry>",6:"<Acknowledge>",7:"<Bell>",8:"<Backspace>",9:"<Horizontal Tab>",10:,11:,12:,13:,14:,15:,16:,17:,18:,19:,20:,
# 21:,22:,23:,24:,25:,26:,27
#
# }

def list_ports():
    try:
        port_name = {}
        ports = list(serial.tools.list_ports.comports())
        with open("../json/config.json", "r") as read_file:
            config = json.loads(read_file.read())
            read_file.close()
        config['COM List'] = [] # clear com port list.
        iterator = 0
        for port in ports:
            iterator+=1
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
            config['COM List'].append(comport_s + ": " + discription) # device name hear.
        if(iterator == 0):
            config['COM List'].append("No Devices Detected") # device name hear.
        print(config)
        with open("../json/config.json", "w") as write_file:
            json.dump(config, write_file)
            write_file.close()
        return port_name

    except Exception as e:
        print(e)
        sys.exit(1)

def validate_command(command,ascii_flag):
    valid_flag = 0
    hex_list = ["1","2","3","4",'5',"6","7","8","9", "0", "a","A", "b", "B", "c", "C", "d", "D", "e", "E", "f", "F"]
    if(len(command) > 0):
        still_parsing = True
        index = 0
        if ascii_flag == 1: #hex format expected

            hex_command=command.replace(" ", "")
            hex_size = len(hex_command)
            #if size not devisible by 4, formate was broken
            if hex_size % 4 != 0:
                valid_flag = 1
            else:
                while still_parsing:
                    # check format for 0xXX
                    #print(hex_command[index] + hex_command[index+1] + hex_command[index+2] + hex_command[index+3])
                    if hex_command[index] != "0" or hex_command[index+1] != "x" or hex_command[index+2] not in hex_list or hex_command[index+3] not in hex_list:
                        valid_flag = 1
                        still_parsing = False
                    #check for end of string
                    elif index+4 == hex_size:
                        still_parsing = False
                    # else increase index and keep parsing
                    else:
                        index= index + 4


        elif ascii_flag == 2: #dec format expected
            try:
                dec_list=command.split()
                for item in dec_list:
                    num = int(item)
                    if num > 255:
                        valid_flag = 1
            except:
                valid_flag = 1


    return valid_flag


def hex_2_ascii(command):
    ascii_string=""
    if(len(command) >> 0):
        still_parsing = True
        index = 0
        while still_parsing:
            found = command[index:].find("0x")
            #print("Found = " + found)
            #print(command[index:])
            if found == -1:
                still_parsing = False
            else:
                byte_value = int(command[index+found+2:index+found+5],16)
                # if byte_value in ascii_chart.keys():
                #     ascii_string = ascii_string + ascii_chart[byte_value]
                if byte_value > 127:
                    ascii_string = ascii_string + "<NA>"
                else:
                    #print(command[index+found+2:index+found+5])
                    ascii_string= ascii_string + bytearray.fromhex(command[index+found+2:index+found+5]).decode()
                index = index+5
    else:
     ascii_string=""
    return ascii_string

def ascii_2_hex(command):
    hex_string=""
    if(len(command) >> 0):
        for char in command:
                byte_char = str.encode(char)
                decoded_value = codecs.encode(byte_char, "hex").decode()
                hex_string = hex_string + "0x" + decoded_value + " "
    else:
     hex_string=""
    return hex_string

def hex_2_dec(command):
    hex_nums = command.split()
    dec_string=""
    for x in hex_nums:
        dec = int(x, 0)
        dec_string = dec_string + str(dec) + " "
    return dec_string


def dec_2_hex(command):
    dec_nums = command.split()
    hex_string=""

    for x in dec_nums:
        hex_value=""
        dec = int(x, 0)
        if dec > 16:
            hex_value = hex(dec)
            hex_string = hex_string + hex_value + " "
        else:
            hex_value = hex(dec)
            hex_string = hex_string + hex_value[0:2] + "0" + hex_value[2] + " "
    return hex_string



def listener(com_port,baudrate,transaction_window,timeout,ascii_flag):
    ser = serial.Serial(com_port, baudrate, timeout=timeout)
    #print("Serial Open")

    response = ser.read(500)
    #print(len(response))
    # response_decode = response.decode("hex")
    ser.close()
    if len(response) > 0:
        print("Serial Response = " + str(response))
        response_s = str(response)
        response_redo = response.hex()
        final_rsp_string = "0x" + response_redo[0:2]
        redo_len = len(response_redo)//2

        for x in range(1,redo_len):
            start = x*2
            end = x*2 + 2
            final_rsp_string = final_rsp_string + " 0x" + response_redo[start:end]
        final_rsp_string = final_rsp_string
        #print("response redo = " + final_rsp_string)
        if ascii_flag == 1:
            rsp_bytes = final_rsp_string  + " "
        elif ascii_flag == 0:
            rsp_bytes = hex_2_ascii(final_rsp_string)  + " "
        elif ascii_flag == 2:
            rsp_bytes = hex_2_dec(final_rsp_string)
        transaction_window.insert(tk.END,str(rsp_bytes))


def send_serial(bytes,com_port,baudrate,transaction_window,timeout,ascii_flag,listen_mode):
    error_string = ""
    try:
        #remove '0x' from bytes
        byte_s1 = bytes.replace("0x", "")
        #remove ' ' from bytes
        byte_s2 = byte_s1.replace(" ", "")
        print("Byte check = " + byte_s2)
        byte_2_send =  bytearray.fromhex(byte_s2)
        print("Bytes to send: " + str(byte_2_send))
        print("Com Port: " + com_port)
        print("Baudrate: " + str(baudrate))
        #transaction_window.insert(tk.END,"TX: " + str(bytes) + "\r\n")
        ser = serial.Serial(com_port, baudrate, timeout=timeout)
        print("Serial Open")
        print("Transmitted gecko_cmd_system_get_bt_address")
        ser.write(byte_2_send)
        response = ser.read(500)
        # response_decode = response.decode("hex")
        ser.close()
        print("Serial Closed")
        print("Serial Response = " + str(response))
        #print("Serial Decoded Response = " + str(response.decode("utf-8")) )
        response_s = str(response)
        response_redo = response.hex()
        final_rsp_string = "0x" + response_redo[0:2]
        redo_len = len(response_redo)//2

        for x in range(1,redo_len):
            start = x*2
            end = x*2 + 2
            final_rsp_string = final_rsp_string + " 0x" + response_redo[start:end]
        print("response redo = " + final_rsp_string)
        #first_qm = response_s.find('\'')
        if len(response_redo) <= 2:  #(first_qm == -1):
            if listen_mode ==  False:
                transaction_window.insert(tk.END,"RX: " + "No Response Received" + "\r\n")
                transaction_window.insert(tk.END,"********************************************" + "\r\n")
        else:
            # second_gm = response_s.find('\'',first_qm +1)
            # unquoted_s = response_s[first_qm+1:second_gm]
            # replace_slash_s = unquoted_s.replace('\\','0')
            # add_spaces_s = replace_slash_s.replace('0x',' 0x')
            # final_rsp_string = add_spaces_s[1:]
            if ascii_flag == 1:
                rsp_bytes = final_rsp_string
            elif ascii_flag == 0:
                rsp_bytes = hex_2_ascii(final_rsp_string)
            elif ascii_flag == 2:
                rsp_bytes = hex_2_dec(final_rsp_string)
            if listen_mode ==  False:
                transaction_window.insert(tk.END,"RX: " + str(rsp_bytes) + "\r\n")
                transaction_window.insert(tk.END,"********************************************" + "\r\n")
            else:
                transaction_window.insert(tk.END,str(rsp_bytes))
    except Exception as e:
        if type(Exception) is type(serial.SerialException):
            print("Serial exception has occured")
        print(e)
        error_string = str(e)
    return error_string

if __name__ == "__main__":
    list_ports()
