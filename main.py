# Tkinter modules
from tkinter import *

# Arduino modules
import serial 
from serial import Serial

# Importing constants
from values import ARDUINO_PORT, BAUD_RATE
from colors import color
from controls import actions

# Modules to control keyboard and mouse
from pynput.mouse import Button as MouseButton, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyController

from threading import Thread
from time import sleep
from time import time
import pickle

# Setup arduino
arduino = Serial(ARDUINO_PORT, BAUD_RATE, timeout=0.1)

# Application configuration
windowSize = [400,450]
windowLocation = [750,200]
windowTitle = "IR Receiver"
window = Tk()

# Pynput configuration
mouse = MouseController()
keyboard = KeyController()

commandOptions = actions
isReceiverRunning = False
performActionFlag = None
toggleBtnText = None
commandBoxText = None
messageLabelText = None
decodedSignal = ''
configMap = {}
lastAction = ''
lastActionTime = 0
thresholdTime = 700
typingThresholdTime = 200
clickThresholdTime = 100
typingIndex = 0

mouseAcceleration = 0.25
mouseStopThresholdTime = 500
mouseInitialSpeed = 5
mouseMaxSpeed = 30
mouseSpeed = 0

PICKLE_FILE_PATH = 'data.pkl'


def exitApplication():
    global isReceiverRunning
    isReceiverRunning = False 
    window.destroy()
    exit()

def resetConfiguration():
    global configMap, messageLabelText
    configMap = {}
    with open(PICKLE_FILE_PATH, 'wb') as handle:
        pickle.dump(configMap, handle, protocol=pickle.HIGHEST_PROTOCOL)
    messageLabelText.set('Saved configurations cleared !')

def saveCommand():
    global configMap
    if decodedSignal == '':
        return
    print(decodedSignal, ' => ', commandBoxText.get())
    configMap[decodedSignal] = commandBoxText.get()
    with open(PICKLE_FILE_PATH, 'wb') as handle:
        pickle.dump(configMap, handle, protocol=pickle.HIGHEST_PROTOCOL)
    messageLabelText.set('Saved !')


def startIRThread():
    global isReceiverRunning, toggleBtnText
    isReceiverRunning = True
    toggleBtnText.set('Stop')
    IR_Thread = Thread(target=startDetection)
    IR_Thread.start()

def stopIRThread():
    global isReceiverRunning, toggleBtnText
    isReceiverRunning = False
    toggleBtnText.set('Start')

def toggleIRThread():
    global isReceiverRunning
    if isReceiverRunning:
        stopIRThread()
    else:
        startIRThread()


def startDetection():
    global decodedSignal, messageLabelText
    while isReceiverRunning:
        try:
            data = arduino.readline()[:-2]
            if data:
                try:
                    # IR signal received 
                    data = data.decode('utf-8')
                    decodedSignal = data
                    # messageLabelText.set('<' + decodedSignal + '>' + ' = ' + str(len(decodedSignal)))
                    messageLabelText.set('<' + decodedSignal + '>')
                    if performActionFlag.get() == 1:
                        if decodedSignal in configMap:
                            performAction(configMap[decodedSignal])
                except Exception as e:
                    print(e)
        except:
            continue

def performTyping(action):
    global typingIndex
    key = action[-1]
    typingMap = {
        '0': ['0'],
        '1': ['1'],
        '2': ['a', 'b', 'c', '2'],
        '3': ['d', 'e', 'f', '3'],
        '4': ['g', 'h', 'i', '4'],
        '5': ['j', 'k', 'l', '5'],
        '6': ['m', 'n', 'o', '6'],
        '7': ['p', 'q', 'r', 's', '7'],
        '8': ['t', 'u', 'v', '8'],
        '9': ['w', 'x', 'y', 'z', '9']
    }
    if key not in typingMap:
        return
    
    currentTime = int(round(time() * 1000))

    if lastAction != action:
        # New key is typed
        typingIndex = 0
        keyboard.press(typingMap[key][typingIndex])
        keyboard.release(typingMap[key][typingIndex])
    else:
        # Same key is typed
        if currentTime - lastActionTime > thresholdTime:
            # Repeat this key
            typingIndex = 0
            keyboard.press(typingMap[key][typingIndex])
            keyboard.release(typingMap[key][typingIndex])
        elif currentTime - lastActionTime > typingThresholdTime:
            # Change to next index
            typingIndex = (typingIndex + 1) % (len(typingMap[key]))
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
            keyboard.press(typingMap[key][typingIndex])
            keyboard.release(typingMap[key][typingIndex])
    

def performAction(action):
    global lastAction, lastActionTime, mouseSpeed
    # TODO: Add implementation here
    print(action)

    

    currentTime = int(round(time() * 1000))
    if action == 'Move mouse left':
        if lastAction != action or  currentTime - lastActionTime > mouseStopThresholdTime:
            mouseSpeed = mouseInitialSpeed
        else:
            mouseSpeed = min(mouseSpeed + mouseAcceleration, mouseMaxSpeed)
        mouse.move(-mouseSpeed, 0)
    elif action == 'Move mouse right':
        if lastAction != action or  currentTime - lastActionTime > mouseStopThresholdTime:
            mouseSpeed = mouseInitialSpeed
        else:
            mouseSpeed = min(mouseSpeed + mouseAcceleration, mouseMaxSpeed)
        mouse.move(mouseSpeed, 0)
    elif action == 'Move mouse up':
        if lastAction != action or  currentTime - lastActionTime > mouseStopThresholdTime:
            mouseSpeed = mouseInitialSpeed
        else:
            mouseSpeed = min(mouseSpeed + mouseAcceleration, mouseMaxSpeed)
        mouse.move(0, -mouseSpeed)
    elif action == 'Move mouse down':
        if lastAction != action or  currentTime - lastActionTime > mouseStopThresholdTime:
            mouseSpeed = mouseInitialSpeed
        else:
            mouseSpeed = min(mouseSpeed + mouseAcceleration, mouseMaxSpeed)
        mouse.move(0, mouseSpeed)
    elif action == 'Mouse left click':
        if lastAction != action or  currentTime - lastActionTime > clickThresholdTime:
            mouse.click(MouseButton.left, 1)
    elif action == 'Mouse right click':
        if lastAction != action or  currentTime - lastActionTime > clickThresholdTime:
            mouse.click(MouseButton.right, 1)
    elif action == 'Mouse double click':
        if lastAction != action or  currentTime - lastActionTime > clickThresholdTime:
            mouse.click(MouseButton.left, 2)
    elif action == 'Space':
        if lastAction != action or  currentTime - lastActionTime > thresholdTime:
            keyboard.press(Key.space)
            keyboard.release(Key.space)
    elif action == 'Enter':
        if lastAction != action or  currentTime - lastActionTime > thresholdTime:
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
    elif action == 'Backspace':
        if lastAction != action or  currentTime - lastActionTime > thresholdTime:
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
    elif action == 'Escape':
        if lastAction != action or  currentTime - lastActionTime > thresholdTime:
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
    elif action == 'Up arrow':
        if lastAction != action or  currentTime - lastActionTime > thresholdTime:
            keyboard.press(Key.up)
            keyboard.release(Key.up)
    elif action == 'Down arrow':
        if lastAction != action or  currentTime - lastActionTime > thresholdTime:
            keyboard.press(Key.down)
            keyboard.release(Key.down)
    elif action == 'Left arrow':
        if lastAction != action or  currentTime - lastActionTime > thresholdTime:
            keyboard.press(Key.left)
            keyboard.release(Key.left)
    elif action == 'Right arrow':
        if lastAction != action or  currentTime - lastActionTime > thresholdTime:
            keyboard.press(Key.right)
            keyboard.release(Key.right)
    elif action == 'Type 0':
        if lastAction != action or  currentTime - lastActionTime > thresholdTime:
            keyboard.press('0')
            keyboard.release('0')
    elif action == 'Type 1':
        if lastAction != action or  currentTime - lastActionTime > thresholdTime:
            keyboard.press('1')
            keyboard.release('1')
    elif action == 'Type a b c 2':
        performTyping(action)
    elif action == 'Type d e f 3':
        performTyping(action)
    elif action == 'Type g h i 4':
        performTyping(action)
    elif action == 'Type j k l 5':
        performTyping(action)
    elif action == 'Type m n o 6':
        performTyping(action)
    elif action == 'Type p q r s 7':
        performTyping(action)
    elif action == 'Type t u v 8':
        performTyping(action)
    elif action == 'Type w x y z 9':
        performTyping(action)
    
    lastAction = action
    lastActionTime = int(round(time() * 1000))



def drawUI():
    global commandBoxText, toggleBtnText, messageLabelText, performActionFlag

    window.geometry(str(windowSize[0]) + "x" + str(windowSize[1]) + "+" + str(windowLocation[0]) + "+" + str(windowLocation[1]) + "")
    window.title(windowTitle)
    window.configure(background=color['Background'])
    
    # Spacer 
    Label(window,font=("times new roman",20),bg=color['Background'],fg=color['NormalText'], width=30).grid(row=0,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)

    # Label to display decodedSignal / messages
    messageLabelText = StringVar()
    messageLabel = Label(window,textvariable=messageLabelText,font=("times new roman",15),bg=color['Background'],fg=color['NormalText'], width=30)
    messageLabel = Label(window,textvariable=messageLabelText,font=("times new roman",15),bg=color['Background'],fg=color['NormalText'], width=30)
    messageLabel.grid(row=1,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
    
    # Dropdown component to assign an action 
    commandBoxText = StringVar(window)
    commandBoxText.set(list(commandOptions)[0])
    commandBox = OptionMenu(window,commandBoxText, *commandOptions,)
    commandBox.config(font=("times new roman",15),bg=color['Background'],fg=color['NormalText'])
    commandBox.configure(anchor='w')
    commandBox.grid(row=2,columnspan=2,sticky=W+E,padx=5,pady=5)
    
    # Save button
    Button(window,text="Save",font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=saveCommand).grid(row=3,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)

    # Spacer 
    Label(window,font=("times new roman",20),bg=color['Background'], width=30).grid(row=4,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)

    # Perform action check button
    performActionFlag = IntVar()
    # checkBox = Checkbutton(window,variable=performActionFlag,text='Enable actions',font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=togglePerformAction)
    checkBox = Checkbutton(window,variable=performActionFlag,text='Enable actions',font=("times new roman",15),bg=color['Background'],fg=color['NormalText'])
    checkBox.grid(row=5,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)

    # Start / Stop IR receiver button 
    toggleBtnText = StringVar()
    toggleBtnText.set('Start')
    toggleBtn = Button(window,textvariable=toggleBtnText,font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=toggleIRThread)
    toggleBtn.grid(row=6,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)

    # Reset button
    Button(window,text="Reset",font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=resetConfiguration).grid(row=7,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
    
    # Exit button
    Button(window,text="Exit",font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=exitApplication).grid(row=8,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
    
    window.mainloop()

def main():
    global configMap
    try:
        with open(PICKLE_FILE_PATH, 'rb') as handle:
            configMap = pickle.load(handle)
            print(configMap)
    except:
        configMap = {}
    drawUI()

if __name__ == '__main__':
    main()




# {
#     '2D0': 'Move mouse left',
#     'CD0': 'Move mouse right',
#     '2F0': 'Move mouse up', 
#     'AF0': 'Move mouse down', 
#     'A70': 'Space', 
#     '5CE9': 'Mouse left click', 
#     'D10': 'Mouse right click', 
#     '1A422E43': 'Move mouse left', 
#     'A23BD824': 'Move mouse right', 
#     'EC27D43D': 'Move mouse up', 
#     '86BD99C': 'Move mouse down',
#     '910': 'Type 0', 
#     '10': 'Type 1', 
#     '810': 'Type a b c 2', 
#     '410': 'Type d e f 3', 
#     'C10': 'Type g h i 4',
#     '210': 'Type j k l 5', 
#     'A10': 'Type m n o 6', 
#     '610': 'Type p q r s 7',
#     'E10': 'Type t u v 8', 
#     '110': 'Type w x y z 9', 
#     '62E9': 'Escape'
# }