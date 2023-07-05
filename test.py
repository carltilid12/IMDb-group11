import tkinter as tk
from tkinter import ttk

# Create the main window
window = tk.Tk()
window.geometry("400x200")

# Create a ttk Style object
style = ttk.Style()
style.theme_use('classic')
# Set the cursor color for the TEntry element
style.configure("TEntry", insertbackground="red")  # Replace "red" with your desired color

# Create a ttk Entry widget
entry = ttk.Entry(window)
entry.pack(padx=20, pady=10)

# Start the Tkinter main loop
window.mainloop()
