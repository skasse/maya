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