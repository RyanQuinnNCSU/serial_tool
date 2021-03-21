# Serial Tool "deBUGger"
> Open source serial terminal optimized for testing embedded devices
<img src="Images/Bugger.png" height="300">

## Table of Contents
1. What is deBUGger?
2. Installation and Start Up
3. deBUGger Walkthrough
4. Modifying the Program
5. Contact info

## 1. What is deBUGger?
Serial is a common method of communication for embedded systems and IOT products from desktop computers. The deBUGger GUI removes the repetitive work of setting serial setting and writing data bytes by saving this information into json profiles. Other key features of this program are summarized below.
- Scan for serial devices (COM ports)
- Converting from HEX, DEC, ASCII
- Automatically send all serial command in a list.
- Write serial log to files
> Note: deBUGger is only supported on Windows, sorry MAC and Linux users.

"deBUGger" is an open source program, meaning you are free to modify the program and add additional features. See section 8 for more details on modifying the Python source code.

<img src="Images/deBUGger_Example.PNG">

## 2. Installation and Start Up
deBUGger can be installed in two ways, via downloading the zip, or cloning the repository. If you have no interest in modifying the source code and wont be using git tracking, then the zip download is the simplest option. Both the http link for Git cloning and the "download zip" button are available under the "code button" on the repo page.
<img src="Images/Download.PNG">

After either cloning or downloading the project, open the "EXE" directory. There you will find the "deBUGger" executable. Double click to start the program.

<img src="Images/Executable.PNG">

After a few seconds of loading the GUI should appear on the screen as shown below.

<img src="Images/Start_Up.PNG">

Now you are ready to start using deBUGger for serial communication.

> Note: For best viewing experience have your display zoom set to 100% (On Win 10: settings->display->scale and layout). If the GUI looks like portions are cropped out, be sure to check this setting.

<img src="Images/Zoom.PNG">

## 3. deBUGger Walkthrough:
This section will provide a walkthrough on how to use deBUGger. The program GUI is broken into 4 sections.

1. Action Buttons:
> Used to save and load serial settings (profiles) to GUI. Also control other serial modes and features.

2. Serial Command List:
> An editable list of serial commands (byte arrays).

3. Serial Transaction Log:
> A terminal showing the bytes transmitted and received over serial.

4. Serial Settings:
> A menu for configuring serial communication settings.  

<img src="Images/Sections.PNG">

### Serial Communication:

Now lets walkthrough basic serial communication using the deBUGger. For the purposes of this walkthrough I am going to use a USB to UART bridge with the RX and TX pins connect by a jumper. Meaning any bytes I send over the serial device will be sent back to my PC.

<img src="Images/Serial_Device.jpg">

To begin serial communication, first we need to select the serial device in the Serial Settings section of the GUI. Start by clicking the refresh button to search for serial devices plugged into your computer.

<img src="Images/refresh.PNG">

Next click on the drop down menu to reveal the device list. For this example I will select the USB to UART Bridge on COM3.

<img src="Images/COM_list.PNG">

After the serial device has been selected, make sure to set the other serial settings to meet your needs. These other settings include the baud rate, byte format (hex,dec,ascii), and the time interval (how long to listen for a serial response after sending a command).

<img src="Images/settings.PNG">

With serial configuration complete, it is now time to start sending serial commands. The first time you open deBUGger a few default serial commands will be provided for you in the command list section. Pressing the ">>" (play) button next to each command will send the command to your chosen serial device.

<img src="Images/play.PNG">

The commands you send over serial can bee seen in the serial transaction log in the middle of the GUI. This log will also show any serial responses before the serial timeout, defined by the time interval setting.

<img src="Images/STL.PNG">

The serial transaction log can be written to a file or cleared by using corresponding action buttons.

 <img src="Images/clear.PNG">

Rather than send each command individually, press the "Loop" button (located in the action buttons section) to run though all the commands in the command list. The loop button will send commands in the order they appear, with time interval separating sending each command.

<img src="Images/loop.PNG">

To modify the command list, press on the "Edit Commands List" button. This will open a new window where commands can be added or removed.

<img src="Images/edit.PNG">
<img src="Images/popup.PNG">

Once you have added all the commands you would like to remove, press "Apply" and your edited commands will be reflected in the command list on the main window. Once you are done editing the command list, close the pop up window.

<img src="Images/new_commands.PNG">

As mentioned previously, you can view serial commands as hex, decimal, or ascii by changing the byte format drop down menu. Doing so will change the commands as they apear in the command list and in the serial transaction log.

<img src="Images/format.PNG">

<img src="Images/conversion.PNG">

If you need to continuously listen for incoming serial bytes press the "listen mode" button (action buttons section). While in 






### Profiles:

### Listen Mode:

### Transaction Window:

## 5. Contact Info
Email: rtquinn2@ncsu.edu
