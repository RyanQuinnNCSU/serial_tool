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
<img src="Images/Sections.PNG">

### Serial Communication:

### Profiles:

### Listen Mode:

### Transaction Window:

## 5. Contact Info
Email: rtquinn2@ncsu.edu
