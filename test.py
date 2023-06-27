import tkinter as tk
from tkinter import ttk

# Create the main window
window = tk.Tk()
window.title("Movie Information")

# Create a Canvas widget
canvas = tk.Canvas(window, width=400, height=400, bg="white")
canvas.pack()

# Define movie information
movie_title = "Inception"
movie_synopsis = "A skilled thief is capable of stealing valuable secrets from deep within the subconscious during the dream state."

# Create a Label widget for movie title
title_label = ttk.Label(canvas, text="Movie Title:", font=("Arial", 12))
canvas.create_window(50, 50, anchor="w", window=title_label)

title_entry = ttk.Entry(canvas, width=30, state="readonly")
title_entry.insert(0, movie_title)
canvas.create_window(200, 50, anchor="w", window=title_entry)

# Create a Label widget for movie synopsis
synopsis_label = ttk.Label(canvas, text="Movie Synopsis:", font=("Arial", 12))
canvas.create_window(50, 100, anchor="w", window=synopsis_label)

synopsis_text = tk.Text(canvas, width=40, height=6)
synopsis_text.insert("1.0", movie_synopsis)
canvas.create_window(200, 120, anchor="w", window=synopsis_text)

# Run the main event loop
window.mainloop()
