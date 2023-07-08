import tkinter as tk
from tkinter import ttk, Tk, Toplevel, Label, Entry, Button, StringVar, messagebox, OptionMenu
from tkinter import messagebox
from tkinter import simpledialog
from PIL import ImageTk, Image
import sqlite3
import os

################################ FUNCTIONS ##################################
# Function to Display the ssearched movie with all the information
def displayMovie(event=None):
    # Get the movie title entered in the search bar
    suggestions_listbox.place_forget()
    search_text = search_var.get()

    # Fetch the movieId of the entered movie title
    conn = sqlite3.connect("imdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT movieId FROM movies WHERE title=?", (search_text,))
    result = cursor.fetchone()
    if result == None:
        cursor.execute("SELECT movieId FROM movies WHERE movieId=?", (search_text,))
        result = cursor.fetchone()
    conn.close()

    if result:
        movieId = result[0]
        global MovieID 
        MovieID = movieId
        # Fetch the movie details using the movieId
        conn = sqlite3.connect("imdb.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE movieId=?", (movieId,))
        movie_details = cursor.fetchone()
        conn.close()

        # Extract the movie details from the fetched data
        movieTitle = movie_details[1] if movie_details[1] is not None else "N/A"
        movieLanguage = movie_details[2] if movie_details[2] is not None else "N/A"
        movieLength_minutes = movie_details[3] if movie_details[3] is not None else 0
        format_movie_length = lambda minutes: f"{minutes // 60}h {minutes % 60}m"
        movieLength = format_movie_length(movieLength_minutes)
        movieYear = movie_details[4] if movie_details[4] is not None else "N/A"
        movieSynopsis = movie_details[5] if movie_details[5] is not None else "N/A"
        movieRatings = movie_details[6] if movie_details[4] is not None else 0.0
        movieCoverPath = movie_details[7]

        # Fetch the genres for the movie using the movieId
        conn = sqlite3.connect("imdb.db")
        cursor = conn.cursor()
        cursor.execute("SELECT genreName FROM genre WHERE movieId=?", (movieId,))
        rows = cursor.fetchall()
        genres = []
        for row in rows:
            if row[0] is not None:
                if isinstance(row[0], tuple):
                    genre_name = "None"
                else:
                    genre_name = row
                    genres.append(genre_name)
        cursor.execute("SELECT producerName FROM producers INNER JOIN produces ON producers.producerID = produces.producerID WHERE produces.movieID=?", (movieId,))
        producerDetails = cursor.fetchone()
        movieProducer = producerDetails[0] if producerDetails is not None else "N/A"
        conn.close()
        # Compile the genres into a list
        stars = "\u2B50" * round(movieRatings)
        genre_list = [genre[0] for genre in genres]
        # Join the genres into a string with '|' separator
        movieGenre = " | ".join(genre_list)

        # Fetch the list of actors and their roles in the movie using the movieId
        conn = sqlite3.connect("imdb.db")
        cursor = conn.cursor()
        cursor.execute("SELECT actors.actorName, casts.character, actors.about FROM actors INNER JOIN casts ON actors.actorId = casts.actorId WHERE casts.movieID=?", (movieId,))
        rows = cursor.fetchall()
        conn.close()
        actors_data = []
        for row in rows:
            actor_name = row[0] if row[0] is not None else "Unknown Actor"
            character = row[1] if row[1] is not None else "Unknown Character"
            about = row[2] if row[2] is not None else "No information available"
            actor_data = [actor_name, character, about]
            actors_data.append(actor_data)
        # Update
        titleValue.config(text=movieTitle)
        languageValue.config(text=movieLanguage)
        lengthValue.config(text=movieLength)
        yearValue.config(text=movieYear)
        ratingsValue.config(text=f"{movieRatings} {stars}")
        synopsisValue.config(state="normal")  # Enable the Text widget
        synopsisValue.delete("1.0", "end")  # Clear existing text
        synopsisValue.insert("1.0", movieSynopsis)  # Insert the fetched movie synopsis
        synopsisValue.config(state="disabled")  # Disable the Text widget after inserting
        genreValue.config(text=movieGenre)  # Update the genre label with the movie genres
        producerValue.config(text=movieProducer)
        # Calculate the y-coordinate for the new director label based on the number of directors and actors
        y_coord_director_label = 400 + len(director_widgets_dict) * 150 + len(actor_widgets_dict) * 150

        # Update the "Director" label's position on the canvas
        infoCanvas.yview_moveto(y_coord_director_label / infoCanvas.winfo_height())
        for row in list(actor_widgets_dict.keys()):
            delete_actor_info(row)

        # Update the actor labels and text fields for each actor in the movie
        for idx, actor_data in enumerate(actors_data):
            create_actor_info(actor_data, idx)
        # Fetch the list of directors and their details for the movie using the movieId
        conn = sqlite3.connect("imdb.db")
        cursor = conn.cursor()
        cursor.execute("SELECT directorName, directorAbout FROM directors INNER JOIN directs ON directors.directorID = directs.directorID WHERE directs.movieID=?", (movieId,))
        rows = cursor.fetchall()
        directors_data = []
        for row in rows:
            directorName = row[0] if row[0] is not None else "Unknown Director"
            directorAbout = row[1] if row[1] is not None else "No information available"
            director_data = [directorName, directorAbout]
            directors_data.append(director_data)
        conn.close()
        for row in list(director_widgets_dict.keys()):
            delete_director_info(row)
        infoCanvas.delete("director_label")
        # Update the director labels and text fields for each director in the movie
        for idx, director_data in enumerate(directors_data):
            create_director_info(director_data, idx)
        # Calculate the y-coordinate for the new director label based on the row


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
        # Check if the movie is bookmarked
        is_bookmarked = is_movie_bookmarked(movieId)

        # Set the image for the bookmark button based on the bookmark status
        bookmark_image = bookmarked_photo if is_bookmarked else bookmark_photo
        bookmark_button.config(image=bookmark_image)
    else:
        # Display a pop-up warning if the movie title does not exist
        messagebox.showwarning("Movie Not Found", f"The movie '{search_text}' does not exist in the database.")

# Function to return the list of movie titles
def getMovies():
    conn = sqlite3.connect("imdb.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM movies")
    movies = [row[1] for row in cursor.fetchall()]

    conn.close()
    return movies

def getMoviesInfo():
    conn = sqlite3.connect("imdb.db")
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT movies.movieID, movies.title, movies.language, \
        movies.year, movies.ratings, \
        directors.directorName, producers.producerName, actors.actorName, genre.genreName \
        FROM movies \
        LEFT JOIN genre ON movies.movieID = genre.movieID \
        LEFT JOIN directs ON movies.movieID = directs.movieID \
        LEFT JOIN directors ON directs.directorID = directors.directorID \
        LEFT JOIN produces ON movies.movieID = produces.movieID \
        LEFT JOIN producers ON produces.producerID = producers.producerID \
        LEFT JOIN casts ON movies.movieID = casts.movieID \
        LEFT JOIN actors ON casts.actorID = actors.actorID") 
    movies = cursor.fetchall()

    conn.close()
    return movies

actor_widgets_dict = {}
# Function to create actor information
def create_actor_info(actor_data, row):
    actor_name, character_name, description = actor_data

    actor_frame = tk.Frame(infoCanvas, bg='#3B3A3B')
    actor_value = ttk.Label(actor_frame, text=f"{actor_name} as {character_name}", font=("Arial", 12, "bold"))
    actor_value .configure(background='#3B3A3B', foreground="white")
    actor_value_info = tk.Text(actor_frame, wrap="word", width=85, height=6)
    actor_value_info.insert("1.0", description)
    actor_value_info.configure(state="disabled", font=("Arial", 9, "italic"))

    # Store references to the actor-related widgets in the dictionary
    actor_widgets_dict[row] = {
        "frame": actor_frame,
        "label": actor_value,
        "text_widget": actor_value_info
    }

    # Calculate the y-coordinate for the new actor info based on the row
    y_coord = 400 + row * 150

    # Create the actor frame and its widgets on the canvas
    actor_frame_id = infoCanvas.create_window(135, y_coord, anchor="w", window=actor_frame)

    # Position the label and text widget inside the frame
    actor_frame.grid_rowconfigure(0, weight=1)
    actor_frame.grid_columnconfigure(0, weight=1)
    actor_value.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    actor_value_info.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    # Update the canvas scroll region to fit all the actors
    canvas_height = 400 + (row) * 150 + 75
    infoCanvas.config(scrollregion=(0, 0, 300, canvas_height))

# Function to delete actor information
def delete_actor_info(row):
    if row in actor_widgets_dict:
        # Get the dictionary containing the widget references for the given row
        widgets = actor_widgets_dict[row]
        # Destroy the widgets and the frame associated with the row
        widgets["label"].destroy()
        widgets["text_widget"].destroy()
        widgets["frame"].destroy()
        # Remove the entry from the dictionary
        del actor_widgets_dict[row]

        # Update the canvas size to fit the remaining actors
        canvas_height = 400 + len(actor_widgets_dict) * 150
        infoCanvas.config(scrollregion=(0, 0, 300, canvas_height))

director_widgets_dict = {}
director_Label = None
def create_director_info(director_data, row):
    global director_Label
    # Destroy the "Director" label if it exists
    for child in infoCanvas.winfo_children():
        if isinstance(child, ttk.Label) and child.cget("text") == "Director:":
            child.destroy()

    director_name, director_about = director_data

    director_frame = tk.Frame(infoCanvas, bg='#3B3A3B')
    director_value = ttk.Label(director_frame, text=f"{director_name}", font=("Arial", 12, "bold"))
    director_value_info = tk.Text(director_frame, wrap="word", width=85, height=6)
    director_value.configure(background='#3B3A3B', foreground="white")
    director_value_info.insert("1.0", director_about)
    director_value_info.configure(state="disabled", font=("Arial", 9, "italic"))

    # Store references to the director-related widgets in the dictionary
    director_widgets_dict[row] = {
        "frame": director_frame,
        "label": director_value,
        "text_widget": director_value_info
    }

    # Calculate the y-coordinate for the new director info based on the row
    num_actors = len(actor_widgets_dict)
    y_coord = 400 + row * 150 + num_actors*150

    if row == 0:
        # Place the "Director" label on the first row
        director_label = ttk.Label(infoCanvas, text="Director:", font=("Arial", 12))
        director_label.configure(background='#28282D', foreground="white")
        infoCanvas.create_window(10, y_coord-50, anchor="w", window=director_label)

    # Create the director frame and its widgets on the canvas
    director_frame_id = infoCanvas.create_window(135, y_coord, anchor="w", window=director_frame)

    # Position the label and text widget inside the frame
    director_frame.grid_rowconfigure(0, weight=1)
    director_frame.grid_columnconfigure(0, weight=1)
    director_value.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    director_value_info.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    canvas_height = 250 + len(director_widgets_dict) * 150 + len(actor_widgets_dict)*150 + 75
    infoCanvas.config(scrollregion=(0, 0, 300, canvas_height))


def delete_director_info(row):
    if row in director_widgets_dict:
        # Get the dictionary containing the widget references for the given row
        widgets = director_widgets_dict[row]
        # Destroy the widgets and the frame associated with the row
        widgets["label"].destroy()
        widgets["text_widget"].destroy()
        widgets["frame"].destroy()
        # Remove the entry from the dictionary
        del director_widgets_dict[row]

        # Update the canvas size to fit the remaining directors
        canvas_height = 400 + len(director_widgets_dict) * 150 + len(actor_widgets_dict)*150 + 75
        infoCanvas.config(scrollregion=(0, 0, 300, canvas_height))

def updateSuggestions(*args):
    # Get the text entered in the search bar
    search_text = search_var.get().lower()  # Convert search text to lowercase
    movies_info = getMoviesInfo()

    unique_movies = set()

    # Filter the movies based on the search text
    for movie in movies_info:
        if any(search_text in str(info).lower() for info in movie):
            unique_movies.add(movie[1])  # Add the movie title to the set
    # Clear the current suggestions in the listbox
    suggestions_listbox.delete(0, tk.END)

    # Update the listbox with the filtered movie titles
    if search_text and unique_movies:
        for movie in unique_movies:
            suggestions_listbox.insert(tk.END, movie)
        suggestions_listbox.place(x=344, y=52)
        suggestions_listbox.lift()
    else:
        suggestions_listbox.place_forget()

def on_suggestion_select(event):
    selected_movie = suggestions_listbox.get(suggestions_listbox.curselection())
    search_var.set(selected_movie)
    # Call the displayMovie function to show the selected movie details
    displayMovie()

def update_canvas_scrollregion(event=None):
    infoCanvas.configure(scrollregion=infoCanvas.bbox('all'))

def sort_column(tree, column, reverse=False):
    children = tree.get_children("")
    current_items = [(tree.set(child, column), child) for child in children]
    # Reverse the existing sort order
    current_items.reverse()
    # Rearrange the items in the Treeview
    for index, (_, child) in enumerate(current_items):
        tree.move(child, "", index)
    # Update the column heading to reflect the new sort order
    tree.heading(column, command=lambda: sort_column(tree, column, not reverse))

def on_movie_select(event):
    # Get the selected item from the Treeview
    selected_item = movie_tree.focus()
    if selected_item:
        # Get the movie title from the selected item
        movie_title = movie_tree.item(selected_item, "values")[0]

        # Set the movie title in the search entry
        search_var.set(movie_title)
        suggestions_listbox.place_forget()

def sort_tree():
    selected_option = sort_var.get()
    movies_info = getMoviesInfo()
    movie_titles = []
    if selected_option == "Ratings":
        movie_titles = sorted(movies_info, key=lambda movie: float(movie[4]) if movie[4] is not None else 0.0, reverse=True)
        movie_titles = [movie[1] for movie in movie_titles if ((movie[1] is not None) and (movie[4] != 0.0))]
    elif selected_option == "Year":
        movie_titles = sorted(movies_info, key=lambda movie: int(movie[3]) if movie[3] is not None else 0, reverse=True)
        movie_titles = [movie[1] for movie in movie_titles if ((movie[1] is not None) and (movie[3] != 0))]
    elif selected_option == "Title":
        movie_titles = [movie[1] for movie in movies_info if movie[1] is not None]
        movie_titles = sorted(movie_titles)
    elif selected_option == "Language":
        movie_titles = sorted(movies_info, key=lambda movie: movie[2] if movie[2] is not None else "")
        movie_titles = [movie[1] for movie in movie_titles if ((movie[1] is not None) and (movie[2] is not None))]
    unique_titles = set()
    sorted_titles = []
    # Iterate over the sorted movie titles
    for movie in movie_titles:
        if movie not in unique_titles:
            sorted_titles.append(movie)
            unique_titles.add(movie)
    # Update the Treeview with the sorted movie titles
    movie_tree.delete(*movie_tree.get_children())
    for title in sorted_titles:
        movie_tree.insert("", "end", values=(title,))

def toggleBookmark(movie_id):
    # Check if the movie is already bookmarked
    is_bookmarked = is_movie_bookmarked(movie_id)

    if is_bookmarked:
        # Movie is already bookmarked, so remove it from the bookmarks
        bookmark_image = bookmark_photo
        remove_movie_from_bookmarks(movie_id)
        bookmark_button.config(image=bookmark_image)
    else:
        # Movie is not bookmarked, so add it to the bookmarks
        bookmark_image = bookmarked_photo
        add_movie_to_bookmarks(movie_id)
        bookmark_button.config(image=bookmark_image)

def is_movie_bookmarked(movie_id):
    conn = sqlite3.connect("imdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM bookmarks WHERE movieID=?", (movie_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def add_movie_to_bookmarks(movie_id):
    conn = sqlite3.connect("imdb.db")
    cursor = conn.cursor()
    # Insert the movie ID into the bookmarks table
    cursor.execute("INSERT INTO bookmarks (movieID) VALUES (?)", (movie_id,))
    
    conn.commit()
    conn.close()

def remove_movie_from_bookmarks(movie_id):
    conn = sqlite3.connect("imdb.db")
    cursor = conn.cursor()
    # Remove the movie ID from the bookmarks table
    cursor.execute("DELETE FROM bookmarks WHERE movieID = ?", (movie_id,))
    
    conn.commit()
    conn.close()

def display_bookmarked_movies():
    # Clear the current content in the treeview
    movie_tree.delete(*movie_tree.get_children())

    # Retrieve the bookmarked movies from the database
    conn = sqlite3.connect("imdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT movies.title FROM bookmarks LEFT JOIN movies ON bookmarks.movieID = movies.movieID")
    bookmarked_movies = cursor.fetchall()
    conn.close()

    # Insert the bookmarked movies into the treeview
    for movie in bookmarked_movies:
        movie_title = movie[0]
        movie_tree.insert("", "end", values=(movie_title,))

def toggle_my_list():
    global my_list_toggle

    if my_list_toggle:
        # Display the sorted movies
        sort_tree()
        my_list_toggle = False
    else:
        # Display the bookmarked movies
        display_bookmarked_movies()
        my_list_toggle = True

def autofillSearchEntry(event=None):
    selected_suggestion = suggestions_listbox.get(0)  # Get the first suggested result
    if selected_suggestion:
        search_var.set(selected_suggestion)  # Set the search entry text to the selected suggestion

# CRUDL FUNCTIONS
def create_movie():
    dialog = tk.Toplevel(window)
    dialog.title("Create Movie")
    dialog.configure(background="#28282D")
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    dialog_width = 450
    dialog_height = 325
    x = (screen_width - dialog_width) // 2
    y = (screen_height - dialog_height) // 2
    dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    # Create labels and entry fields for the movie attributes
    labels = ["Movie ID:", "Title:", "Language:", "Length:", "Year:", "Ratings:", "Genre:", "Synopsis:", "Movie Cover:"]
    entries = []
    for i, label_text in enumerate(labels):
        label = ttk.Label(dialog, text=label_text, background='#28282D', foreground="white", font=("Arial ", 11))
        label.grid(row=i, column=0, padx=5, pady=5)

        entry = ttk.Entry(dialog, width=55)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)

    def save_movie():
        try:
            conn = sqlite3.connect("imdb.db")
            cursor = conn.cursor()
            # Retrieve the values from the entry fields
            movie_id = int(entries[0].get())
            cursor.execute("SELECT COUNT(*) FROM movies WHERE movieID=?", (movie_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showwarning("Invalid Input", "Movie ID already exists.")
                dialog.focus_force()
                conn.close()
                return
            
            title = entries[1].get()
            language = entries[2].get()
            length = entries[3].get()
            year = entries[4].get()
            ratings = entries[5].get()
            genre_input = entries[6].get()
            synopsis = entries[7].get()
            movie_cover = entries[8].get()

            if any(value is None or value == "" for value in [title, language, length, year, ratings, genre_input, synopsis, movie_cover]):
                raise ValueError("Invalid input")
            
            length = int(length)
            year = int(year)
            ratings = float(ratings)
            genres = [genre.strip() for genre in genre_input.split(',')]

            cursor.execute("INSERT INTO movies (movieID, title, language, length, year, synopsis, ratings, movieCover) \
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (movie_id, title, language, length, year, synopsis, ratings, movie_cover))
            for genre in genres:
                cursor.execute("INSERT INTO genre (movieID, genreName) VALUES (?, ?)", (movie_id, genre))
            # Commit the values and close the dialog window and the connection
            conn.commit()
            conn.close()
            search_var.set(title)
            displayMovie()
            sort_tree()
            dialog.destroy()
        except ValueError:
            # Catch ValueError if there are any input value conversion errors
            messagebox.showwarning("Invalid Input", "Please enter valid values for movie ID, length, year, and ratings.")
            dialog.focus_force()

    save_button = tk.Button(dialog, text="Save", command=save_movie)
    save_button.grid(row=len(labels), columnspan=2, padx=5, pady=10)

def update_movie():
    global MovieID
    movieID = MovieID
    dialog = tk.Toplevel(window)
    dialog.title("Update Movie")
    dialog.configure(background="#28282D")
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    dialog_width = 450
    dialog_height = 325
    x = (screen_width - dialog_width) // 2
    y = (screen_height - dialog_height) // 2
    dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    # Retrieve the movie details based on the global variable movieID
    conn = sqlite3.connect("imdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE movieID=?", (movieID,))
    movie = cursor.fetchone()
    cursor.execute("SELECT genreName FROM genre WHERE movieID=?", (movieID,))
    genres = [genre[0] for genre in cursor.fetchall()]
    conn.close()

    # Create labels and entry fields for the movie attributes
    labels = ["Title:", "Language:", "Length:", "Year:", "Ratings:", "Genre:", "Synopsis:", "Movie Cover:"]
    entries = []
    for i, label_text in enumerate(labels):
        label = ttk.Label(dialog, text=label_text, background='#28282D', foreground="white", font=("Arial ", 11))
        label.grid(row=i, column=0, padx=5, pady=5)

        entry = ttk.Entry(dialog, width=55)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)

    # Set the initial values in the entry fields
    entries[0].insert(0, movie[1]) 
    entries[1].insert(0, movie[2])
    entries[2].insert(0, str(movie[3]))
    entries[3].insert(0, str(movie[4]))
    entries[5].insert(0, ", ".join(genres))
    entries[4].insert(0, str(movie[6]))
    entries[6].insert(0, movie[5])
    entries[7].insert(0, movie[7])

    def save_movie():
        try:
            conn = sqlite3.connect("imdb.db")
            cursor = conn.cursor()

            # Retrieve the updated values from the entry fields
            title = entries[0].get()
            language = entries[1].get()
            length = entries[2].get()
            year = entries[3].get()
            ratings = entries[4].get()
            genre_input = entries[5].get()
            synopsis = entries[6].get()
            movie_cover = entries[7].get()

            if any(value is None or value == "" for value in [title, language, length, year, ratings, genre_input, synopsis, movie_cover]):
                raise ValueError("Invalid input")

            length = int(length)
            year = int(year)
            ratings = float(ratings)
            genres = [genre.strip() for genre in genre_input.split(',')]

            cursor.execute("UPDATE movies SET title=?, language=?, length=?, year=?, synopsis=?, ratings=?, movieCover=? WHERE movieID=?",
                        (title, language, length, year, synopsis, ratings, movie_cover, movieID))

            # Delete and Insert new genre records for the movie
            cursor.execute("DELETE FROM genre WHERE movieID=?", (movieID,))
            for genre in genres:
                cursor.execute("INSERT INTO genre (movieID, genreName) VALUES (?, ?)", (movieID, genre))
            # Commit the values and close the dialog window and the connection
            conn.commit()
            conn.close()
            search_var.set(title)
            displayMovie()
            sort_tree()
            dialog.destroy()
        except ValueError:
            # Catch ValueError if there are any input value conversion errors
            messagebox.showwarning("Invalid Input", "Please enter valid values for length, year, and ratings.")
            dialog.focus_force()

    save_button = tk.Button(dialog, text="Save", command=save_movie)
    save_button.grid(row=len(labels), columnspan=2, padx=5, pady=10)

def delete_movie():
    global MovieID
    movie_id = MovieID
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this movie?")
    if confirm:
        try:
            conn = sqlite3.connect("imdb.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM genre WHERE movieID=?", (movie_id,))
            #cursor.execute("DELETE FROM directs WHERE movieID=?", (movie_id,))
            #cursor.execute("DELETE FROM casts WHERE movieID=?", (movie_id,))
            #cursor.execute("DELETE FROM produces WHERE movieID=?", (movie_id,))
            cursor.execute("DELETE FROM movies WHERE movieID=?", (movie_id,))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            messagebox.showinfo("Movie Deleted", "The movie has been deleted successfully.")
            movies_list = getMovies()
            movie_title = movies_list[0]
            search_var.set(movie_title)
            displayMovie() if movies_list else None
            sort_tree()
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while deleting the movie:\n" + str(e))
    else:
        messagebox.showinfo("Deletion Cancelled", "Deletion has been cancelled.")

def display_movie():
    dialog = tk.Toplevel(window)
    dialog.title("Display Movies")
    dialog.configure(background="#28282D")

    # Create a frame to hold the Treeview
    frame = tk.Frame(dialog)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, height=30)
    tree["columns"] = ("Movie ID", "Title", "Language", "Length", "Year", "Synopsis", "Ratings", "Movie Cover", "Genre")

    # Configure column headings
    tree.heading("#0", text="")
    tree.heading("Movie ID", text="Movie ID")
    tree.heading("Title", text="Title")
    tree.heading("Language", text="Language")
    tree.heading("Length", text="Length")
    tree.heading("Year", text="Year")
    tree.heading("Synopsis", text="Synopsis")
    tree.heading("Ratings", text="Ratings")
    tree.heading("Movie Cover", text="Movie Cover")
    tree.heading("Genre", text="Genre")

    # Configure column widths
    tree.column("#0", width=0, stretch=False)
    tree.column("Movie ID", width=80)
    tree.column("Title", width=150)
    tree.column("Language", width=150)
    tree.column("Length", width=50)
    tree.column("Year", width=50)
    tree.column("Synopsis", width=250)
    tree.column("Ratings", width=50)
    tree.column("Movie Cover", width=150)
    tree.column("Genre", width=150)

    # Configure treeview size
    tree.pack(fill="both", expand=True)

    # Retrieve data from the "movies" table
    conn = sqlite3.connect("imdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT movies.movieID, movies.title, movies.language, movies.length, movies.year, \
                    movies.synopsis, movies.ratings, movies.movieCover, GROUP_CONCAT(genre.genreName) \
                    FROM movies LEFT JOIN genre ON movies.movieID = genre.movieID \
                    GROUP BY movies.movieID")
    movies_data = cursor.fetchall()
    conn.close()

    # Insert movie data into the Treeview
    for movie in movies_data:
        movie_id, title, language, length, year, synopsis, ratings, movie_cover, genres = movie
        tree.insert("", "end", iid=movie_id, values=(movie_id, title, language, length, year, synopsis, ratings, movie_cover, genres))

    # Set the column width to fit the content
    tree["displaycolumns"] = ("Movie ID", "Title", "Language", "Length", "Year", "Synopsis", "Ratings", "Movie Cover", "Genre")
    tree["show"] = "headings"

def create_actor():
    print("Performing Create action for Actors")

def update_actor():
    print("Performing Update action for Actors")

def delete_actor():
    print("Performing Delete action for Actors")

def display_actor():
    print("Performing Display action for Actors")

actions = {
    ("Create", "Movie"): create_movie,
    ("Update", "Movie"): update_movie,
    ("Delete", "Movie"): delete_movie,
    ("Display", "Movie"): display_movie,
    ("Create", "Actor"): create_actor,
    ("Update", "Actor"): update_actor,
    ("Delete", "Actor"): delete_actor,
    ("Display", "Actor"): display_actor,
}

def perform_action():
    crudl = crudl_var.get()
    entity = entity_var.get()

    # Get the corresponding action from the dictionary and call it
    action = actions.get((crudl, entity))
    if action:
        action()

################################## MAIN #####################################

# MAIN WINDOW
window = tk.Tk()
window.title("IMDb")
window.configure(bg='#181818')

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

##### STYLES #######

style = ttk.Style()
style.theme_use('clam')
style.map("Custom.TButton",
          background=[("active", "gray")])
style.map("TButton",
          background=[("active", "gray")])
style.configure("TButton", 
                background="black", 
                foreground="black",
                highlightcolor="black",
                padding=1,
                borderwidth=0,
                relief="flat",
                selectbackground="red",
                selectforeground="white")
style.configure("Custom.TButton", 
                background="black", 
                foreground="#232323",
                highlightcolor="#232323",
                padding=1,
                borderwidth=0,
                relief="flat")
style.configure("Search.TEntry", 
                padding = 8,
                highlightcolor="",
                relief="flat",
                selectbackground="white",
                selectforeground="black", 
                fieldbackground="#28282D",
                insertcolor="#d7d7d2",
                highlightbackground="",
                borderwidth=0,
                bordercolor="black",
                foreground="white")
style.map("TCombobox", fieldbackground=[("readonly", "#28282D")],
                selectbackground=[("readonly", "#28282D")])
style.configure("TCombobox",
                foreground="white",
                background="black",
                selectbackground="#28282D",
                selectforeground="white",
                fieldbackground="#28282D",
                arrowsize=0,
                relief="flat",
                padding=5)
style.map("Treeview",
    background=[("selected", "#c3c3c3"), ("active", "#00FF00")],
    foreground=[("selected", "#000000"), ("active", "#000000")],
    font=[("selected", ("Arial", 10, "bold")), ("active", ("Arial", 10))],
    fieldbackground=[("selected", "#CCCCCC"), ("active", "#EEEEEE")])
style.configure("Treeview", 
                font=("Arial", 8), 
                foreground="white", 
                background="#28282D",
                fieldbackground="#28282D")
style.map("TScrollbar",
          background=[("active", "gray"), ("!active", "#28282D")],
          arrowcolor=[("active", "white"), ("!active", "black")])
style.configure("TScrollbar",
                background="#CCCCCC",
                padding=10,
                width=12)

##### FIRST ROW ########

# Load the logo image
logo_path = "assets\IMDB_Logo_2016 1.png"  # Replace with the actual path to your logo image file
logo_image = Image.open(logo_path)
logo_photo = ImageTk.PhotoImage(logo_image)
info_button = ttk.Button(window, image=logo_photo, width=10, style="TButton", \
                         command=lambda: messagebox.showinfo("Info", ("IMBD group 11 - Lavesores, Tabanas, Tilid", MovieID)))
info_button.grid(row=0, column=0, padx=(0), pady=15, columnspan=2)

# Create the search bar
search_var = tk.StringVar()
search_var.trace_add('write', updateSuggestions)  # Track changes in the search bar text
search_entry = ttk.Entry(window, textvariable=search_var, width=70, font=("Arial ", 11), style="Search.TEntry")
search_entry.grid(row=0, column=2, padx=(40,0), pady=10)
search_entry.bind("<Return>", lambda event: (displayMovie(), suggestions_listbox.lift()))
search_entry.bind("<FocusOut>", lambda event: suggestions_listbox.place_forget())
search_entry.bind("<Tab>", lambda event: (autofillSearchEntry(), displayMovie()))

suggestions_listbox = tk.Listbox(window, width=96, height=5)
suggestions_listbox.bind("<<ListboxSelect>>", lambda event: on_suggestion_select(event) if suggestions_listbox.curselection() else None)

# Create Search Label
search_path = "assets\\search.png"  # Replace with the actual path to your logo image file
search_image = Image.open(search_path)
search_photo = ImageTk.PhotoImage(search_image)
search_button = tk.Button(window, image=search_photo, font=("Arial", 12), border=0, command=displayMovie)
search_button.grid(row=0, column=3, padx=(0,40), pady=10)
search_button.configure(background='black', foreground="white")

# Create My List
myList_path = "assets\\myList.png"  # Replace with the actual path to your logo image file
myList_image = Image.open(myList_path)
myList_photo = ImageTk.PhotoImage(myList_image)
my_list_toggle = False
myList_button = ttk.Button(window, image=myList_photo, width=10, style="TButton", \
                         command=toggle_my_list)
myList_button.grid(row=0, column=4, padx=(0), pady=10)

# Sort Dropdown
sort_var = tk.StringVar()
sort_var.set("Title")
sort_dropdown = ttk.Combobox(window, textvariable=sort_var, values=["Title", "Language", "Year", "Ratings"], state="readonly", style="TCombobox")
sort_dropdown.grid(row=0, column=5, padx=(0,60), pady=10)
sort_dropdown.bind("<<ComboboxSelected>>", lambda event: sort_tree())

# Row 1 Background
row1 = tk.Frame(window, bg="black")
row1.grid(row=0, column=0, sticky="nsew", columnspan=6)
row1.lower()

# Create a Treeview widget to display the list of movies
movies_frame = ttk.Frame(window)
movies_frame.grid(row=1, column=4, padx=(5, 70), pady=(15,25), rowspan=5, columnspan=2)
movie_tree = ttk.Treeview(movies_frame, columns=("Movies"), show="headings", height=29)
movie_tree.heading("Movies", text="Title", anchor='w')
movie_tree.column("Movies", anchor='w', width=260)
movie_tree.pack(side=tk.LEFT, fill=tk.BOTH)
movie_tree.heading("Movies", text="List of Movies", command=lambda c="Movies": sort_column(movie_tree, c))
movie_tree.bind("<<TreeviewSelect>>", on_movie_select)

# Populate the Treeview with movie data
movies = getMovies()
for movie in movies:
    movie_tree.insert("", "end", values=(movie,))
movie_tree.bind("<Double-Button-1>", lambda event: (displayMovie() if movie_tree.focus() else None,
                                                    suggestions_listbox.place_forget()))
sort_tree()

#### MOVIE INFO ####

#Movie Cover
coverCanvas = tk.Canvas(window, width=270, height=440, bg='#232323', highlightbackground='#232323')
coverCanvas.grid(row=1, column=0, padx=15, pady=(20, 20), rowspan=2, columnspan=2)

movieCoverPath = "assets\\houseOfDragon.png"
movieCoverVar = (movieCoverPath)
coverImage = tk.PhotoImage(file=movieCoverVar)
movieCover = coverCanvas.create_image(135, 200, image=coverImage)
currentCoverImage = coverImage

MovieID = 1234567890
# Bookmark Button
bookmark_path = "assets\\bookmark.png"
bookmarked_path = "assets\\bookmarked.png"
bookmark_image = Image.open(bookmark_path)
bookmarked_image = Image.open(bookmarked_path)
bookmark_photo = ImageTk.PhotoImage(bookmark_image)
bookmarked_photo = ImageTk.PhotoImage(bookmarked_image)
is_bookmarked = is_movie_bookmarked(1234567890)
initial_image = bookmarked_photo if is_bookmarked else bookmark_photo
style.configure("Custom.TButton", background="#232323", foreground="#232323",highlightcolor="#232323",
                padding=1, borderwidth=0, relief="flat")
bookmark_button = ttk.Button(window, image=initial_image, width=10, style="Custom.TButton", \
                         command=lambda: (toggleBookmark(MovieID), display_bookmarked_movies() if my_list_toggle else None))
bookmark_button.grid(row=2, column=0, padx=(0), pady=(320,0), columnspan=2)

# CRUDL
crudl_var = tk.StringVar()
crudl_var.set("Create")
crudl_dropdown = ttk.Combobox(window, textvariable=crudl_var, values=["Create", "Update", "Delete", "Display"], state="readonly", style="TCombobox")
crudl_dropdown.grid(row=3, column=0, padx=0, pady=0)

# Entity
entity_var = tk.StringVar()
entity_var.set("Movie")
entity_dropdown = ttk.Combobox(window, textvariable=entity_var, values=["Movie", "Producer", "Actor", "Director"], state="readonly", style="TCombobox")
entity_dropdown.grid(row=3, column=1, padx=0, pady=0)

# Select
select_path = "assets\select.png"  # Replace with the actual path to your logo image file
select_image = Image.open(select_path)
select_photo = ImageTk.PhotoImage(select_image)
select_button = ttk.Button(window, image=select_photo, width=10, style="Custom.TButton", command=perform_action)
select_button.grid(row=5, column=0, padx=(0), pady=(0,70), columnspan=2)

# Default Movie Details
movieTitle = "House of the Dragon"
movieLanguage = "English (United States)"
movieLength = "1h 47m"
movieYear = "2022"
movieRatings = 8.5
movieGenre = "Action | Adventure | Drama"
movieSynopsis = "An internal succession war within House Targaryen at the height of its power, 172 years before the birth of Daenerys Targaryen."

movieActor = (("Matt Smith", "Prince Daemon Targaryen", "Matt Smith is an English actor who shot to fame in the UK aged 26 when he was cast by producer Steven Moffat as the Eleventh Doctor in the BBC's iconic science-fiction adventure series Doctor Who (2005)."),\
              ("Emma D'arcy", "Queen Rhaenyra Targaryen", "British actor born in London. Emma D'Arcy is an actor and theatre-maker. Emma studied at the Ruskin School of Art. They are also the Joint Artistic Director of the Forward Arena Theatre Company. Their performance on stage in Christopher Shinn's 'Against' alongside actor Ben Whishaw was described as \"exceedingly likeable and sensitive\""),\
                ("Olivia Cooke", "Queen Alicent Hightower", "Olivia Cooke was born and raised in Oldham, a former textile manufacturing town in Greater Manchester, North West England. She comes from a family of non-actors; her father, John, is a retired police officer, and her mother is a sales representative. Cooke attended Royton and Crompton Secondary School and studied drama at Oldham Sixth Form College, leaving before the end of her A-levels to star in Blackout."),\
                    )
movieDirector = (("Ryan J. Condalv", "Ryan J. Condal is known for House of the Dragon (2022), Rampage (2018) and Colony (2016)."))
movieProducer = "Warner Bros"
currentMovieActor = movieActor
currentMovieDirector = movieDirector

# Movie Information
# Canvas
infoCanvas = tk.Canvas(window, width=750, height=600, bg='#28282D', highlightbackground='#28282D')
infoCanvas.grid(row=1, column=2, padx=0, pady=(0,10), columnspan=2, rowspan=5)

# Create a frame to hold the contents of the canvas
infoFrame = tk.Frame(infoCanvas, bg='#28282D')
infoCanvas.create_window(0, 0, anchor='nw', window=infoFrame)

# Configure the scrollbar
scrollbar = ttk.Scrollbar(window, orient='vertical', command=infoCanvas.yview)
scrollbar.place(relx=1.0, rely=0, relheight=1.0, anchor='ne')
infoCanvas.configure(yscrollcommand=scrollbar.set)
infoCanvas.bind("<Enter>", lambda event: infoCanvas.bind_all('<MouseWheel>', lambda e:
    infoCanvas.yview_scroll(-1 * (e.delta // 120), 'units')))
infoCanvas.bind("<Leave>", lambda event: infoCanvas.unbind_all('<MouseWheel>'))
# Bind the function to the canvas size change event
infoCanvas.bind('<Configure>', update_canvas_scrollregion)

# Movie Title
titleLabel = ttk.Label(infoCanvas, text="Movie Title: ", font=("Arial ", 11))
titleLabel.configure(background='#28282D', foreground="white")
infoCanvas.create_window(10, 25, anchor="w", window=titleLabel)
titleValue = ttk.Label(infoCanvas, text=movieTitle, font=("Arial Black", 18, "bold"))
titleValue.configure(background='#28282D', foreground="white")
infoCanvas.create_window(135, 25, anchor="w", window=titleValue)
# Movie Language
languageLabel = ttk.Label(infoCanvas, text="Language: ", font=("Arial", 11))
languageLabel.configure(background='#28282D', foreground="white")
infoCanvas.create_window(10, 55, anchor="w", window=languageLabel)
languageValue = ttk.Label(infoCanvas, text=movieLanguage, font=("Arial", 10, "bold"))
languageValue.configure(background='#28282D', foreground="white")
infoCanvas.create_window(135, 55, anchor="w", window=languageValue)
# Movie Length
lengthLabel = ttk.Label(infoCanvas, text="Length: ", font=("Arial", 11))
lengthLabel.configure(background='#28282D', foreground="white")
infoCanvas.create_window(10, 75, anchor="w", window=lengthLabel)
lengthValue = ttk.Label(infoCanvas, text=movieLength, font=("Arial", 12))
lengthValue.configure(background='#28282D', foreground="white")
infoCanvas.create_window(135, 75, anchor="w", window=lengthValue)
# Movie Year
yearLabel = ttk.Label(infoCanvas, text="Year:", font=("Arial", 11))
yearLabel.configure(background='#28282D', foreground="white")
infoCanvas.create_window(10, 100, anchor="w", window=yearLabel)
yearValue = ttk.Label(infoCanvas, text=movieYear, font=("Arial", 11))
yearValue.configure(background='#28282D', foreground="white")
infoCanvas.create_window(135, 100, anchor="w", window=yearValue)
# Movie Ratings
ratingsLabel = ttk.Label(infoCanvas, text="Ratings:", font=("Arial", 11))
ratingsLabel.configure(background='#28282D', foreground="white")
infoCanvas.create_window(10, 125, anchor="w", window=ratingsLabel)
stars = "\u2B50" * round(movieRatings)
ratingsValue = ttk.Label(infoCanvas, text=f"{movieRatings} {stars}", font=("Arial", 11))
ratingsValue.configure(background='#28282D', foreground="white")
infoCanvas.create_window(135, 125, anchor="w", window=ratingsValue)
# Movie Genre
genreLabel = ttk.Label(infoCanvas, text="Genre:", font=("Arial", 11))
genreLabel.configure(background='#28282D', foreground="white")
infoCanvas.create_window(10, 155, anchor="w", window=genreLabel)
genreValue = ttk.Label(infoCanvas, text=movieGenre, font=("Arial", 12, "bold"))
genreValue.configure(background='#28282D', foreground="white")
infoCanvas.create_window(135, 155, anchor="w", window=genreValue)
# Movie Synopsis
synopsisLabel = ttk.Label(infoCanvas, text="Synopsis:", font=("Arial", 11))
synopsisLabel .configure(background='#28282D', foreground="white")
infoCanvas.create_window(10, 210, anchor="w", window=synopsisLabel)
synopsisValue = tk.Text(infoCanvas, wrap="word", width=76, height=4, bg='#28282D', highlightthickness=0, borderwidth=0,fg='white')
synopsisValue.insert("1.0", movieSynopsis)
synopsisValue.configure(state="disabled", font=("Arial", 11,"italic"))
infoCanvas.create_window(135, 230, anchor="w", window=synopsisValue)
# Movie Producer
producerLabel = ttk.Label(infoCanvas, text="Producer:", font=("Arial", 11))
producerLabel.configure(background='#28282D', foreground="white")
infoCanvas.create_window(10, 310, anchor="w", window=producerLabel)
producerValue = ttk.Label(infoCanvas, text=movieProducer, font=("Arial", 11, "bold"))
producerValue.configure(background='#28282D', foreground="white")
infoCanvas.create_window(135, 310, anchor="w", window=producerValue)
# Movie Cast
castLabel = ttk.Label(infoCanvas, text="Cast:", font=("Arial", 11))
castLabel.configure(background='#28282D', foreground="white")
infoCanvas.create_window(10, 345, anchor="w", window=castLabel)
for idx, actor_info in enumerate(movieActor):
    create_actor_info(actor_info, idx)
create_director_info(movieDirector, 0)
# Update the scrollable region initially
update_canvas_scrollregion()
##### RUN #######
# Main Window
window.mainloop()
