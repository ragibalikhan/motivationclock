import tkinter as tk
from tkinter import ttk
from datetime import datetime
import requests
import sys
import win32gui
import win32con

# API endpoint for fetching quotes
api_url = "http://127.0.0.1:5000/api/motivational-quotes"

# Function to fetch a random quote from the API
def fetch_random_quote():
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            quote = response.json().get("quote", "")
            return quote
        else:
            print(f"Failed to fetch quote. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching the quote: {str(e)}")

# Function to update the time
def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time)  # Update every 1000 milliseconds (1 second)

# Function to update the quote
def update_quote():
    quote = fetch_random_quote()
    quote_label.config(text=f"Motivational Quote: {quote}")
    root.after(30000, update_quote)  # Update every 30000 milliseconds (30 seconds)

# Get the handle of the desktop window
def get_desktop_handle():
    return win32gui.GetDesktopWindow()

# Set clock window as a child of the desktop window
def set_clock_on_desktop():
    desktop_handle = get_desktop_handle()
    if desktop_handle:
        win32gui.SetParent(root.winfo_id(), desktop_handle)
        win32gui.SetWindowLong(root.winfo_id(), win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(root.winfo_id(), win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(root.winfo_id(), 0, 255, win32con.LWA_ALPHA)

# Create the main window
root = tk.Tk()
root.title("Futuristic Clock Widget")
root.geometry("420x250")
root.configure(bg="#333333")  # Background color
root.overrideredirect(True)  # Remove window decorations
root.attributes("-topmost", True)  # Keep the window on top of others

# Create and configure labels
time_label = ttk.Label(root, font=("DS-Digital", 48), foreground="#FFD700", background="#333333")
quote_label = ttk.Label(root, font=("Arial", 14), wraplength=400, justify="center", foreground="#FFF", background="#333333")

# Pack labels into the window
time_label.pack(pady=20)
quote_label.pack()

# Run the initial updates
update_time()
update_quote()

# Set clock window as a child of the desktop
set_clock_on_desktop()

# Start the Tkinter event loop
root.mainloop()
