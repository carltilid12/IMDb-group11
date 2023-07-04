import tkinter as tk
from PIL import Image, ImageTk

# Create the main window
window = tk.Tk()
window.title("Movie Details")
window.geometry("800x600")

# Load the background image
background_image = Image.open("assets\\bossBaby.png")
background_image = background_image.resize((800, 600), Image.ANTIALIAS)  # Resize the image to fit the window

# Create a Tkinter PhotoImage from the PIL image
background_photo = ImageTk.PhotoImage(background_image)

# Create a Canvas widget to display the background image
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()

# Display the background image on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)

# Run the Tkinter main loop
window.mainloop()
