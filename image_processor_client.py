# image_processor_client.py
from tkinter import *
from tkinter import ttk
import requests
server_name = "http://127.0.0.1:5000"
# server_name = "http://vcm-13874.vm.duke.edu:5000"


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
    image_choice_box = ttk.Combobox(root, textvariable=image_choice)
    image_choice_box.grid(column=1, row=1)
    image_choice_box['values'] = ("acl1.jpg", "acl2.jpg", "esophagus1.jpg",
                                  "esophagus2.jpg", "synpic50411.jpg",
                                  "synpic51041.jpg", "synpic51042.jpg",
                                  "upj1.jpg", "upj2.jpg")
    image_choice_box.state(["readonly"])

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
    def upload_button():
        image_name = image_selection.get()
        print("You've selected {}".format(image_name))
        upload_image(image_name)
        # close window
        # upload status window
        return

    def back_button():
        sub_upload.destroy()
        return

    sub_upload = Toplevel()  # sets up main window
    sub_upload.title("Upload New")
    sub_upload.columnconfigure(0, pad=8)
    sub_upload.columnconfigure(1, pad=8)
    sub_upload.columnconfigure(2, pad=8)

    # Add main label
    top_label = ttk.Label(sub_upload, text="Upload New")
    top_label.grid(column=0, row=0, columnspan=2, sticky=W)

    # Image selection
    select_label = ttk.Label(sub_upload, text="Choose an image:")
    select_label.grid(column=0, row=1)
    image_selection = StringVar()
    image_entry = ttk.Entry(sub_upload, textvariable=image_selection, width=30)
    image_entry.grid(column=1, row=1)

    # Add buttons
    upload_btn = ttk.Button(sub_upload, text="Upload", command=upload_button)
    upload_btn.grid(column=0, row=6)
    back_btn = ttk.Button(sub_upload, text="Back", command=back_button)
    back_btn.grid(column=1, row=6)

    return


def upload_image(image_name):
    new_image = {"image": image_name}
    r = requests.post(server_name + "/api/upload_image", json=new_image)
    if r.status_code != 200:
        print("Error: {} - {}".format(r.status_code, r.text))
    else:
        print("Success: {}".format(r.text))


if __name__ == "__main__":
    main_window()
