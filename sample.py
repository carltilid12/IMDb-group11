import tkinter as tk
import sqlite3
from tkinter import messagebox

def create_table():
    conn = sqlite3.connect("sample.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)")

    conn.commit()
    conn.close()

def add_contact():
    name = name_entry.get()
    email = email_entry.get()

    conn = sqlite3.connect("sample.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO contacts (name, email) VALUES (?, ?)", (name, email))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Contact added successfully!")

def show_contacts():
    conn = sqlite3.connect("sample.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()

    conn.close()

    for contact in contacts:
        messagebox.showinfo("Contact", f"Name: {contact[1]}\nEmail: {contact[2]}")

# Create the main window
window = tk.Tk()
window.title("SQLite Database with Tkinter")
window.geometry("300x200")

# Create labels and entry fields
name_label = tk.Label(window, text="Name:")
name_label.pack()

name_entry = tk.Entry(window)
name_entry.pack()

email_label = tk.Label(window, text="Email:")
email_label.pack()

email_entry = tk.Entry(window)
email_entry.pack()

# Create buttons
create_table_button = tk.Button(window, text="Create Table", command=create_table)
create_table_button.pack()

add_contact_button = tk.Button(window, text="Add Contact", command=add_contact)
add_contact_button.pack()

show_contacts_button = tk.Button(window, text="Show Contacts", command=show_contacts)
show_contacts_button.pack()

# Run the main event loop
window.mainloop()
