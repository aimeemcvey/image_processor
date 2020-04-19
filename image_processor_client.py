# image_processor_client.py
from tkinter import *
from tkinter import ttk


def main_window():
    def upload_new():
        upload_new_window()
        return

    def cancel_button():
        root.destroy()
        return

    root = Tk()  # sets up main window
    root.title("Image Processor")
    root.columnconfigure(0, pad=8)
    root.columnconfigure(1, pad=8)
    root.columnconfigure(2, pad=8)

    # Add main label
    top_label = ttk.Label(root, text="Image Processor")
    top_label.grid(column=0, row=0, columnspan=2, sticky=W)

    # Image selection
    select_label = ttk.Label(root, text="Select an image:")
    select_label.grid(column=0, row=1)

    image_choice = StringVar()
    organ_choice_box = ttk.Combobox(root, textvariable=image_choice)
    organ_choice_box.grid(column=1, row=1)
    organ_choice_box['values'] = ()

    # Add Radiobuttons
    action_label = ttk.Label(root, text="Action:")
    action_label.grid(column=0, row=2)
    action = StringVar()
    ttk.Radiobutton(root, text="Invert", variable=action,
                    value="invert").grid(column=1, row=2, sticky=W)
    ttk.Radiobutton(root, text="Display", variable=action,
                    value="display").grid(column=1, row=3, sticky=W)
    ttk.Radiobutton(root, text="Download", variable=action,
                    value="download").grid(column=1, row=4, sticky=W)

    # Add buttons
    ok_btn = ttk.Button(root, text="Ok")  # command=ok_button)
    ok_btn.grid(column=0, row=6)
    cancel_btn = ttk.Button(root, text="Cancel", command=cancel_button)
    cancel_btn.grid(column=1, row=6)
    upload_btn = ttk.Button(root, text="Upload New", command=upload_new)
    upload_btn.grid(column=2, row=6)

    root.mainloop()
    return


def upload_new_window():
    def back_button():
        root.destroy()
        return

    root = Tk()  # sets up main window
    root.title("Upload New")
    root.columnconfigure(0, pad=8)
    root.columnconfigure(1, pad=8)
    root.columnconfigure(2, pad=8)

    # Add main label
    top_label = ttk.Label(root, text="Upload New")
    top_label.grid(column=0, row=0, columnspan=2, sticky=W)

    # Image selection
    select_label = ttk.Label(root, text="Choose an image:")
    select_label.grid(column=0, row=1)
    image_choice = StringVar()
    image_entry = ttk.Entry(root, textvariable=image_choice, width=30)
    image_entry.grid(column=1, row=1)

    # Add buttons
    upload_btn = ttk.Button(root, text="Upload")  # command=upload_button)
    upload_btn.grid(column=0, row=6)
    back_btn = ttk.Button(root, text="Back", command=back_button)
    back_btn.grid(column=1, row=6)

    return


if __name__ == "__main__":
    main_window()
