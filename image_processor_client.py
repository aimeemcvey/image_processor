# image_processor_client.py
from tkinter import *
from tkinter import ttk


def main_window():
    root = Tk()  # sets up main window
    root.title("Image Processor")

    # Add main label
    top_label = ttk.Label(root, text="Image Processor")
    top_label.grid(column=0, row=0, columnspan=2, sticky=W)

    # Add Radiobuttons
    action = StringVar()
    ttk.Radiobutton(root, text="Upload", variable=action,
                    value="upload").grid(column=0, row=2, sticky=W)
    ttk.Radiobutton(root, text="Invert", variable=action,
                    value="invert").grid(column=0, row=3, sticky=W)
    ttk.Radiobutton(root, text="Display", variable=action,
                    value="display").grid(column=0, row=4, sticky=W)
    ttk.Radiobutton(root, text="Download", variable=action,
                    value="download").grid(column=0, row=5, sticky=W)

    # Add buttons
    ok_btn = ttk.Button(root, text="Ok")   # command=ok_button)
    ok_btn.grid(column=1, row=6)
    cancel_btn = ttk.Button(root, text="Cancel")  # command=cancel_button)
    cancel_btn.grid(column=2, row=6)

    root.mainloop()
    return


if __name__ == "__main__":
    main_window()