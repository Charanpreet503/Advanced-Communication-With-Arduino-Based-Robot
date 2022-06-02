import serial.tools.list_ports 
import time
from tkinter import *

def rgb(rgb):
    """
    Function will convert rgb to hexadecimal format
    :param rgb:
    :return:
    """
    return "#%02x%02x%02x" % rgb

def bluetooth_connect_menu():
    global enterSec
    global root, connectButton, refreshButton
    root = Tk()
    root.title("Bluetooth Controller")
    root.minsize(width=700, height=500)
    root.geometry("700x500")
    root.config(bg= rgb((39, 54, 59)))

    portLable = Label(root, text= "Avaliable Ports: ", fg="white", font=('Aileron Regular',12), bg= rgb((39, 54, 59)))
    portLable.place(relx=0,rely=0, relwidth=0.25,relheight=0.1)

    baudeLable = Label(root, text= "Baude Rate: ", fg="white", font=('Aileron Regular',12), bg= rgb((39, 54, 59)))
    baudeLable.place(relx=0,rely=0.1, relwidth=0.25,relheight=0.1)

    refreshButton = Button(root, text= "Refresh", bg=rgb((253, 206, 170)), height= 2, width= 10, command= updateComPorts)
    refreshButton.place(relx=0.69,rely=0.03, relwidth=0.19,relheight=0.07)

    connectButton = Button(root, text= "Connect", bg=rgb((253, 206, 170)), height= 2, width= 10, state= "disabled", command=connection)
    connectButton.place(relx=0.69,rely=0.110, relwidth=0.19,relheight=0.07)

    enterSecLabel = Label(root, text="Enter number of seconds:", fg="white", font=('Aileron Regular',12), bg= rgb((39, 54, 59)))
    enterSecLabel.place(relx=0.1,rely=0.23, relwidth=0.25,relheight=0.1)

    enterSec = Entry(root, width=5)
    enterSec.insert(0, "2")
    enterSec.place(relx=0.46,rely=0.23, relwidth=0.1,relheight=0.1)

    forwardButton = Button(root, text="Forward", bg= rgb((153, 185, 152)), fg='black',font=('Aileron Regular',15),command=forward)
    forwardButton.place(relx=0.38,rely=0.4, relwidth=0.25,relheight=0.1)

    backwardButton = Button(root, text="Backward", bg=rgb((153, 185, 152)), fg='black',font=('Aileron Regular',15),command=backward)
    backwardButton.place(relx=0.38,rely=0.66, relwidth=0.25,relheight=0.1)

    leftButton = Button(root, text="Left", bg=rgb((153, 185, 152)), fg='black',font=('Aileron Regular',15),command=left)
    leftButton.place(relx=0.10,rely=0.53, relwidth=0.25,relheight=0.1)

    rightButton = Button(root, text="Right", bg=rgb((153, 185, 152)), fg='black',font=('Aileron Regular',15),command=right)
    rightButton.place(relx=0.66,rely=0.53, relwidth=0.25,relheight=0.1)

    stopButton = Button(root, text="Stop", bg=rgb((235, 73, 96)), fg='black',font=('Aileron Regular',15), command=stop)
    stopButton.place(relx=0.38,rely=0.53, relwidth=0.25,relheight=0.1)

    baudeSelect()
    updateComPorts()


def checkConnect(args):
    """
    checks the if baudeMenu and comOption are selected
    if none or one of them is not selected the connect button is disables
    but if both the com port and baude rate are selected the connect button is activated
    :param args:
    :return:
    """
    if "-" in baudeMenu.get() or "-" in comOption.get():    # if nothing is selected the connect button will disable it self
         connectButton["state"] = "disabled"
    else:                                                   # else the state will be active when both the com port and baud rate is selected
        connectButton["state"] = "active"


def baudeSelect():
    """
    displays dropdown menu for selcting baud rate
    default baude rate is set to 9600
    :return:
    """
    global baudeMenu, dropBaude
    baudeMenu = StringVar()

    # List of all the baud rates that the user can select
    baudeList = ["-","110", "300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200", "128000" , "256000"]
    baudeMenu.set(baudeList[7]) #default baud rate 9600

    dropBaude = OptionMenu(root, baudeMenu, *baudeList, command= checkConnect)
    dropBaude.config(width=20, bg=rgb((244, 131, 125)))
    dropBaude.place(relx=0.20,rely=0.1, relwidth=0.25,relheight=0.1)

def connection():
    """
    * Activate and Deactivate the connect baud rate, comports, refresh and connect buttons depending
    up weather port and baud rate is selcted or not.
    * if the com port and baude rate is selected then it will try to open the selected com port on the
    selected baud rate with a timeout of 1 seconds
    :return:
    """
    global ser, forwardButton, backwardButton

    if connectButton["text"] in "Disconnect":
        connectButton["text"] = "Connect"
        refreshButton["state"] = "active"
        dropBaude["state"] = "active"
        comDrop["state"] = "active"
    else:
        connectButton["text"] = "Disconnect"
        refreshButton["state"] = "disabled"
        dropBaude["state"] = "disabled"
        comDrop["state"] = "disabled"
        port = comOption.get()
        baude = baudeMenu.get()
        try:
            ser = serial.Serial(port, baude, timeout= 1)
        except:
            pass


def updateComPorts():
    """
    This function will show a drop down henu for com ports at which we will communicate with our robot
    :return:
    """
    global comOption, comDrop
    ports = serial.tools.list_ports.comports()
    print(ports)
    coms = [com[0] for com in ports]
    print(coms)
    coms.insert(0, "-") #we are adding "-" at index 0 to show if we do not have any com ports

    # refreshing com port menu
    # preventing overlapping com ports menu as thay will be updating after pressing the refresh button
    # it will try to destroy if there are any previous option menu
    try:
        comDrop.destroy()
    except:
        pass

    comOption = StringVar()
    comOption.set(coms[0])
    comDrop = OptionMenu(root, comOption, *coms, command= checkConnect)
    comDrop.config(width= 10, bg=rgb((244, 131, 125)))
    comDrop.place(relx=0.20,rely=0, relwidth=0.25,relheight=0.1)
    checkConnect(0)

def forward():
    global ser, enterSec
    print("Forward command executed")
    try:
        seconds = enterSec.get()
        print(seconds)
        if userInputCheck(seconds) == True:
            ttime = time.time() + int(seconds)
            print(ttime)
            while time.time() < ttime:
                ser.write(b'F')

            ttimw2 = time.time() + 1
            while time.time() < ttimw2:
                ser.write(b'S')
            print("Stop Executed")
    except:
        pass

def backward():
    global ser, enterSec
    print("Backward command executed")
    try:
        ser.write(b'B')
        seconds = enterSec.get()
        print(seconds)
        if userInputCheck(seconds) == True:
            ttime = time.time() + int(seconds)
            print(ttime)
            while time.time() < ttime:
                ser.write(b'B')
            #time.sleep(int(seconds))
            ttimw2 = time.time() + 1
            while time.time() < ttimw2:
                ser.write(b'S')
            print("Stop Executed")
    except:
        pass

def right():
    global ser, enterSec
    print("Right command executed")
    try:
        ser.write(b'R')
        seconds = enterSec.get()
        print(seconds)
        if userInputCheck(seconds) == True:
            ttime = time.time() + int(seconds)
            print(ttime)
            while time.time() < ttime:
                ser.write(b'R')
            #time.sleep(int(seconds))
            ttimw2 = time.time() + 1
            while time.time() < ttimw2:
                ser.write(b'S')
            print("Stop Executed")
    except:
        pass

def left():
    global ser, enterSec
    print("Left command executed")
    try:
        ser.write(b'L')
        seconds = enterSec.get()
        print(seconds)
        if userInputCheck(seconds) == True:
            ttime = time.time() + int(seconds)
            print(ttime)
            while time.time() < ttime:
                ser.write(b'L')
            #time.sleep(int(seconds))
            ttimw2 = time.time() + 1
            while time.time() < ttimw2:
                ser.write(b'S')
            print("Stop Executed")
    except:
        pass

def stop():
    global ser, enterSec
    print("Stop command executed")
    try:
        ser.write(b'S')
        seconds = enterSec.get()
        print(seconds)
        if userInputCheck(seconds) == True:
            time.sleep(int(seconds))
            ser.write(b'S')
            print("Stop Executed")
    except:
        pass

def userInputCheck(userInput):
    """
    This function will check if the argument passed in the function is integer or not
    :param userInput:
    :return: bool
    """
    try:
        int(userInput)
        return True
    except:
        messagebox.showerror("Error","Please enter a valid integer", icon= 'error')
        return False


bluetooth_connect_menu()

root.mainloop()
