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

<img src="Images/Serial_Device.JPG">

The first time you lanch debugger, a few default serial commands will be provided in the Command list. To send each command  

### Profiles:

### Listen Mode:

### Transaction Window:

## 5. Contact Info
Email: rtquinn2@ncsu.edu
