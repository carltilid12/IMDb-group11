import tkinter as tk
from tkinter import ttk

# Function to get the movie titles (you can modify this to retrieve data from your database)
def getMovies():
    return ["Movie 1", "Movie 2", "Movie 3", "Movie 4", "Movie 5"]

# Function to update the search suggestion dropdown based on the current text in the search bar
def update_suggestions():
    search_text = search_var.get()
    if search_text:
        suggestions = [movie for movie in movies if search_text.lower() in movie.lower()]
        suggestion_var.set(suggestions)
        suggestion_listbox.place(x=110, y=65 + search_entry.winfo_height())  # Place below the search bar
    else:
        suggestion_listbox.place_forget()  # Hide the dropdown if no active text

# Create the main window
window = tk.Tk()
window.title("Movie Information")

# Create a search bar
search_var = tk.StringVar()
search_entry = ttk.Entry(window, textvariable=search_var, width=40)
search_entry.place(x=0, y=0)

# Get movie titles
movies = getMovies()

# Create a listbox for search suggestions
suggestion_var = tk.StringVar()
suggestion_listbox = tk.Listbox(window, listvariable=suggestion_var, width=40, height=5)

# Update suggestions when search bar text changes
search_var.trace_add("write", lambda *args: update_suggestions())

# Run the main event loop
window.mainloop()
