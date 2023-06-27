import tkinter as tk
from tkinter import ttk, Tk, Toplevel, Label, Entry, Button, StringVar, messagebox, OptionMenu
from tkinter import messagebox
from tkinter import simpledialog
from PIL import ImageTk, Image
import sqlite3

################################ FUNCTIONS ##################################

################################## MAIN #####################################

# MAIN WINDOW
window = tk.Tk()
window.title("IMDb")
window.configure(bg='#333030')

# Get the screen width and height
screen_width = window.winfo_screenwidth()      
screen_height = window.winfo_screenheight()

# Set the desired window size
window_width = 1366                         
window_height = 768

# Calculate the window position
x = (screen_width - window_width) // 2          
y = (screen_height - window_height) // 2

# Set the window position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.state('zoomed')      # Maximize the window

##### FIRST ROW ########

# Load the logo image
logo_path = "assets\IMDB_Logo_2016 1.png"  # Replace with the actual path to your logo image file
logo_image = Image.open(logo_path)
logo_photo = ImageTk.PhotoImage(logo_image)

# Create the logo label
logo_label = ttk.Label(window, image=logo_photo)
logo_label.grid(row=0, column=0, padx=(50, 100), pady=10)

# Create the menu button
menu_button = ttk.Button(window, text="Menu")
menu_button.grid(row=0, column=1, padx=100, pady=10)

# Create the search bar
search_entry = ttk.Entry(window, width=75)
search_entry.grid(row=0, column=2, padx=100, pady=10, sticky="ew")
##search_entry.bind("<Return>", search)

# Create the home button
home_button = ttk.Button(window, text="Home")
home_button.grid(row=0, column=3, padx=100, pady=10)

# Create the My List button
mylist_button = ttk.Button(window, text="My List")
mylist_button.grid(row=0, column=4, padx=100, pady=10, sticky="e")

##### RUN #######

# Run the main event loop
window.mainloop()
