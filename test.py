import tkinter as tk
from tkinter import ttk

def create_tab(tab_control, title, content):
    frame = ttk.Frame(tab_control)
    label = ttk.Label(frame, text=content)
    label.pack(padx=10, pady=10)
    tab_control.add(frame, text=title)

def main():
    root = tk.Tk()
    root.title("Simple Tabbed Interface")
    root.geometry("400x300")

    tab_control = ttk.Notebook(root)
    tab_control.pack(fill=tk.BOTH, expand=True)

    create_tab(tab_control, "Tab 1", "This is content for Tab 1")
    create_tab(tab_control, "Tab 2", "Welcome to Tab 2")
    create_tab(tab_control, "Tab 3", "Content of Tab 3 goes here")

    root.mainloop()

if __name__ == "__main__":
    main()

# fork test >> Hi carl!
