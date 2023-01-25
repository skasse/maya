import tkinter as tk

# Create the main window
root = tk.Tk()

# Create a variable to track whether the loop should continue running
keep_running = True

# Create a function that will be called when the user clicks the "Quit" button
def quit_loop():
    global keep_running
    keep_running = False
    root.destroy()

# Create a button that will be used to stop the loop
button = tk.Button(root, text="Quit", command=quit_loop)
button.pack()

# Run the loop
while keep_running:
    print('running')
    root.update_idletasks()
    root.update()

#####################################################################
#####################################################################
#####################################################################
#####################################################################
#####################################################################





import maya.cmds as mc

keep_running = True

def quit_loop(self):
    global keep_running
    keep_running = False
    print('stop running')

def start_loop(self):
    while keep_running:
        print('running')





class my_window(object):

    def __init__(self) -> None:
        
        self.window = "My Window"
        self.title = "Window Title"
        self.size = (400, 400)

        if cmds.window(self.window, exists = True):
            cmds.deleteUI(self.window, window=True)
        
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        cmds.columnLayout()
        cmds.button(label="Cancel", command = quit_loop)
        cmds.button(label="Start", command = start_loop)

        cmds.showWindow()

myWindow = my_window()



import maya.cmds as cmds
import time

keep_running = True
def quit_loop():
    global keep_running
    keep_running = False


cmds.progressWindow(isInterruptable=1)
while keep_running:
    for i in range(10):
        if cmds.progressWindow(query=1, isCancelled=1):
            quit_loop
            break
        print(i)
        time.sleep(1)

    if cmds.progressWindow(query=1, isCancelled=1):
        quit_loop
        break

cmds.progressWindow(endProgress=1)