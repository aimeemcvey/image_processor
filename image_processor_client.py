# image_processor_client.py
from tkinter import *
from tkinter import ttk


def main_window():
    root = Tk()  # sets up main window
    root.title("Image Processor")

    # Add main label
    top_label = ttk.Label(root, text="Image Processor")
    top_label.grid(column=0, row=0, columnspan=2, sticky=W)

    root.mainloop()
    return


if __name__ == "__main__":
    main_window()