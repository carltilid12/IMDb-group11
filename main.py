import tkinter as tk
from tkinter import ttk, Tk, Toplevel, Label, Entry, Button, StringVar, messagebox, OptionMenu
from tkinter import messagebox
from tkinter import simpledialog
from PIL import ImageTk, Image
import sqlite3
import os

################################ FUNCTIONS ##################################
def displayMovie(event=None):
    # Get the movie title entered in the search bar
    search_text = search_var.get()

    # Fetch the movieId of the entered movie title
    conn = sqlite3.connect("imdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT movieId FROM movies WHERE title=?", (search_text,))
    result = cursor.fetchone()
    conn.close()

    if result:
        movieId = result[0]

        # Fetch the movie details using the movieId
        conn = sqlite3.connect("imdb.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE movieId=?", (movieId,))
        movie_details = cursor.fetchone()
        conn.close()

        # Extract the movie details from the fetched data
        movieTitle = movie_details[1]
        movieLanguage = movie_details[2]
        movieLength_minutes = movie_details[3]
        format_movie_length = lambda minutes: f"{minutes // 60}h {minutes % 60}m"
        movieLength = format_movie_length(movieLength_minutes)
        movieYear = movie_details[4]
        movieSynopsis = movie_details[5]
        movieRatings = movie_details[6]
        movieCoverPath = movie_details[7]

        # Fetch the genres for the movie using the movieId
        conn = sqlite3.connect("imdb.db")
        cursor = conn.cursor()
        cursor.execute("SELECT genreName FROM genre WHERE movieId=?", (movieId,))
        genres = cursor.fetchall()
        conn.close()
        # Compile the genres into a list
        genre_list = [genre[0] for genre in genres]
        # Join the genres into a string with '|' separator
        movieGenre = " | ".join(genre_list)
        
        titleValue.config(text=movieTitle)
        languageValue.config(text=movieLanguage)
        lengthValue.config(text=movieLength)
        yearValue.config(text=movieYear)
        ratingsValue.config(text=movieRatings)
        synopsisValue.config(state="normal")  # Enable the Text widget
        synopsisValue.delete("1.0", "end")  # Clear existing text
        synopsisValue.insert("1.0", movieSynopsis)  # Insert the fetched movie synopsis
        synopsisValue.config(state="disabled")  # Disable the Text widget after inserting
        genreValue.config(text=movieGenre)  # Update the genre label with the movie genres
        
        global current_cover_image
        
        try:
            if movieCoverPath and os.path.exists(movieCoverPath):
                coverImage = tk.PhotoImage(file=movieCoverPath)
            else:
                raise FileNotFoundError  # Raise an error if the image file is not found
        except FileNotFoundError:
            coverImage = tk.PhotoImage(file="assets\\Null.png")
        coverCanvas.itemconfig(movieCover, image=coverImage)
        current_cover_image = coverImage    
        
    else:
        # Display a pop-up warning if the movie title does not exist
        messagebox.showwarning("Movie Not Found", f"The movie '{search_text}' does not exist in the database.")


def getMovies():
    conn = sqlite3.connect("imdb.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM movies")
    movies = [row[1] for row in cursor.fetchall()]

    conn.close()
    return movies

def updateSuggestions(*args):
    # Get the text entered in the search bar
    search_text = search_var.get()
    movies = getMovies()
    # Filter the movies based on the search text
    filtered_movies = [movie for movie in movies if search_text.lower() in movie.lower()]

    # Clear the current suggestions in the listbox
    suggestions_listbox.delete(0, tk.END)

    # Update the listbox with the filtered movie titles
    if search_text and filtered_movies:
        for movie in filtered_movies:
            suggestions_listbox.insert(tk.END, movie)
        suggestions_listbox.place(x=483, y=40)
        suggestions_listbox.lift()
    else:
        suggestions_listbox.place_forget()
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
search_var = tk.StringVar()
search_var.trace_add('write', updateSuggestions)  # Track changes in the search bar text
search_entry = ttk.Entry(window, textvariable=search_var, width=50)
search_entry.grid(row=0, column=2, padx=10, pady=10)
search_entry.bind("<Return>", displayMovie)
search_entry.bind("<FocusOut>", lambda event: suggestions_listbox.place_forget())

suggestions_listbox = tk.Listbox(window, width=50, height=5)
def on_suggestion_select(event):
    selected_movie = suggestions_listbox.get(suggestions_listbox.curselection())
    search_var.set(selected_movie)
    # Call the displayMovie function to show the selected movie details
    displayMovie()

suggestions_listbox.bind("<<ListboxSelect>>", lambda event: on_suggestion_select(event) if suggestions_listbox.curselection() else None)


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

movieCoverPath = "assets\\houseOfDragon.png"
movieCoverVar = (movieCoverPath)
coverImage = tk.PhotoImage(file=movieCoverVar)
movieCover = coverCanvas.create_image(150, 200, image=coverImage)
currentCoverImage = coverImage

#Movie Information
infoCanvas = tk.Canvas(window, width=600, height=400, bg='#433E3E', highlightbackground='#433E3E')
infoCanvas.grid(row=1, column=2, padx=10, pady=10, columnspan=1)

movieTitle = "House of the Dragon"
movieLanguage = "English (United States)"
movieLength = "1h 47m"
movieYear = "2022"
movieRatings = '8.5'
movieGenre = "Action | Adventure | Drama" #split(tuplegenre)
movieSynopsis = "An internal succession war within House Targaryen at the height of its power, 172 years before the birth of Daenerys Targaryen."

# Movie Title
titleLabel = ttk.Label(infoCanvas, text="Movie Title: ", font=("Arial", 12))
infoCanvas.create_window(25, 25, anchor="w", window=titleLabel)
titleValue = ttk.Label(infoCanvas, text=movieTitle, font=("Arial", 12))
infoCanvas.create_window(150, 25, anchor="w", window=titleValue)
# Movie Language
languageLabel = ttk.Label(infoCanvas, text="Language: ", font=("Arial", 12))
infoCanvas.create_window(25, 50, anchor="w", window=languageLabel)
languageValue = ttk.Label(infoCanvas, text=movieLanguage, font=("Arial", 12))
infoCanvas.create_window(150, 50, anchor="w", window=languageValue)
# Movie Length
lengthLabel = ttk.Label(infoCanvas, text="Length: ", font=("Arial", 12))
infoCanvas.create_window(25, 75, anchor="w", window=lengthLabel)
lengthValue = ttk.Label(infoCanvas, text=movieLength, font=("Arial", 12))
infoCanvas.create_window(150, 75, anchor="w", window=lengthValue)
# Movie Year
yearLabel = ttk.Label(infoCanvas, text="Year:", font=("Arial", 12))
infoCanvas.create_window(25, 100, anchor="w", window=yearLabel)
yearValue = ttk.Label(infoCanvas, text=movieYear, font=("Arial", 12))
infoCanvas.create_window(150, 100, anchor="w", window=yearValue)
# Movie Ratings
ratingsLabel = ttk.Label(infoCanvas, text="Ratings:", font=("Arial", 12))
infoCanvas.create_window(25, 125, anchor="w", window=ratingsLabel)
ratingsValue = ttk.Label(infoCanvas, text=movieRatings, font=("Arial", 12))
infoCanvas.create_window(150, 125, anchor="w", window=ratingsValue)
# Movie Genre
genreLabel = ttk.Label(infoCanvas, text="Genre:", font=("Arial", 12))
infoCanvas.create_window(25, 150, anchor="w", window=genreLabel)
genreValue = ttk.Label(infoCanvas, text=movieGenre, font=("Arial", 12))
infoCanvas.create_window(150, 150, anchor="w", window=genreValue)
# Movie Synopsis
synopsisLabel = ttk.Label(infoCanvas, text="Synopsis:", font=("Arial", 12))
infoCanvas.create_window(25, 175, anchor="w", window=synopsisLabel)
synopsisValue = tk.Text(infoCanvas, wrap="word", width=50, height=8)
synopsisValue.insert("1.0", movieSynopsis)
synopsisValue.configure(state="disabled")
infoCanvas.create_window(150, 225, anchor="w", window=synopsisValue)

##### RUN #######

# Main Window
window.mainloop()
