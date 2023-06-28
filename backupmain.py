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
logo_label = ttk.Label(window, image=logo_photo, background='#333030')
logo_label.grid(row=0, column=0, padx=0, pady=10)

# Create the menu button
menu_button = ttk.Button(window, text="Menu")
menu_button.grid(row=0, column=1, padx=10, pady=10)

# Create the search bar
search_entry = ttk.Entry(window, width=75)
search_entry.grid(row=0, column=2, padx=10, pady=10)
##search_entry.bind("<Return>", search)

# Create the home button
home_button = ttk.Button(window, text="Home")
home_button.grid(row=0, column=3, padx=10, pady=10)

# Create the My List button
mylist_button = ttk.Button(window, text="My List")
mylist_button.grid(row=0, column=4, padx=10, pady=10)

#### MOVIE INFO ####

#Movie Cover
coverCanvas = tk.Canvas(window, width=300, height=400, bg='#333030', highlightbackground='#333030')
coverCanvas.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

movieCoverPath = "assets\houseOfDragon.png"
movieCoverVar = (movieCoverPath)
coverImage = tk.PhotoImage(file=movieCoverVar)
movieCover = coverCanvas.create_image(150, 200, image=coverImage)

#Movie Information
infoCanvas = tk.Canvas(window, width=600, height=400, bg='#433E3E', highlightbackground='#433E3E')
infoCanvas.grid(row=1, column=2, padx=10, pady=10, columnspan=1)

movieTitle = "House of the Dragon"
movieYear = "2022"
movieSynopsis = "An internal succession war within House Targaryen at \
                 the height of its power, 172 years before the birth of Daenerys Targaryen."
movieGenre = "Action | Adventure | Drama" #for i in range
movieLanguage = "English"
movieLength = "1h 47m"

titleLabel = ttk.Label(infoCanvas, text="Movie Title:", font=("Arial", 12))
infoCanvas.create_window(25, 25, anchor="w", window=titleLabel)
titleValue = ttk.Label(infoCanvas, text=movieTitle, font=("Arial", 12))
infoCanvas.create_window(150, 25, anchor="w", window=titleValue)

yearLabel = ttk.Label(infoCanvas, text="Year:", font=("Arial", 12))
infoCanvas.create_window(25, 50, anchor="w", window=titleLabel)
yearValue = ttk.Label(infoCanvas, text=movieYear, font=("Arial", 12))
infoCanvas.create_window(150, 50, anchor="w", window=titleValue)

synopsisLabel = ttk.Label(infoCanvas, text="Synopsis:", font=("Arial", 12))
infoCanvas.create_window(25, 50, anchor="w", window=titleLabel)
synopsisValue = ttk.Label(infoCanvas, text=moveSynopsis, font=("Arial", 12))
infoCanvas.create_window(150, 50, anchor="w", window=titleValue)

##### RUN #######

# Main Window
window.mainloop()
