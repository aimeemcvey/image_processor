# image_processor_client.py
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import requests
import base64
import io
import matplotlib.image as mpimg
import json
from matplotlib import pyplot as plt
import binascii
import os.path
from os import path
import PIL
from PIL import Image, ImageTk
from skimage.io import imsave

server_name = "http://127.0.0.1:5000"


# server_name = "http://vcm-13874.vm.duke.edu:5000"


def main_window():
    def upload_new():
        upload_new_window()
        return

    def cancel_button():
        root.destroy()
        return

    def ok_button():
        if image_choice.get() == "":
            no_selection_message = "Please select an image."
            messagebox.showerror(title="Selection Error",
                                 message=no_selection_message,
                                 icon="error")
            return
        else:
            message_out = "You have selected to {} {}.\n" \
                          "Continue?" \
                .format(action.get(), image_choice.get())
            response = messagebox.askyesno(message=message_out,
                                           icon="question")
        if response is False:
            return
        elif response is True:
            if action.get() == "invert":
                invert_out = invert_image(image_choice.get())
                if invert_out is True:
                    success_message = "Image inverted successfully"
                    messagebox.showinfo(title="Inversion Success",
                                        message=success_message)
                else:
                    messagebox.askretrycancel(title="Inversion Failure",
                                              message=invert_out,
                                              icon="error")
                    return
            else:
                b64_to_convert = fetch_b64(image_choice.get())
                try:
                    nd_to_disp = b64_string_to_ndarray(b64_to_convert)
                except binascii.Error:
                    messagebox.askretrycancel(title="Failure to Find Image",
                                              message=b64_to_convert,
                                              icon="error")
                    return
                if action.get() == "display":
                    # img_out = display_image(nd_to_disp)
                    tk_image, pixel_size = ndarray_to_tkinter_image(nd_to_disp)
                    display_window(tk_image, pixel_size, image_choice.get())
                    return
                if action.get() == "download":
                    f = create_filename(image_choice.get())
                    img_out = b64_to_image_file(b64_to_convert, f)
                    if img_out is True:
                        success_message = "Image downloaded successfully"
                        messagebox.showinfo(title="Download Success",
                                            message=success_message)
        return

    def update_list_combobox():
        image_list = get_image_list()
        image_choice_box['values'] = image_list

    root = Tk()  # sets up main window
    root.title("Image Processor")
    root.columnconfigure(0, pad=8)
    root.columnconfigure(1, pad=8)
    root.columnconfigure(2, pad=8)

    # Add main label
    top_label = ttk.Label(root, text="Image Processor",
                          font='Helvetica 10 bold')
    top_label.grid(column=0, row=0, columnspan=2, sticky=W)

    # Image selection
    select_label = ttk.Label(root, text="Select an image:")
    select_label.grid(column=0, row=1)

    image_choice = StringVar()
    image_choice_box = ttk.Combobox(root, textvariable=image_choice,
                                    postcommand=update_list_combobox)
    image_choice_box.grid(column=1, row=1)
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
    ok_btn = ttk.Button(root, text="Ok", command=ok_button)
    ok_btn.grid(column=0, row=6)
    cancel_btn = ttk.Button(root, text="Cancel", command=cancel_button)
    cancel_btn.grid(column=1, row=6)
    upload_btn = ttk.Button(root, text="Upload New", command=upload_new)
    upload_btn.grid(column=2, row=6)

    root.mainloop()
    return


def get_image_list():
    r = requests.get(server_name + "/api/image_list")
    if r.status_code != 200:
        list_failure_message = "Failed to acquire image list: {} - {}" \
            .format(r.status_code, r.text)
        return list_failure_message
    else:
        return json.loads(r.text)


def invert_image(image_name):
    image_to_invert = {"image": image_name}
    r = requests.post(server_name + "/api/invert_image", json=image_to_invert)
    if r.status_code != 200:
        failure_message = "Image inversion failed: {} - {}" \
            .format(r.status_code, r.text)
        return failure_message
    else:
        return True


def fetch_b64(image_name):
    r = requests.get(server_name + "/api/fetch_b64/{}".format(image_name))
    if r.status_code != 200:
        failure_message = "Image collection failed: {} - {}" \
            .format(r.status_code, r.text)
        return failure_message
    else:
        return json.loads(r.text)


def b64_string_to_ndarray(b64_string):
    image_bytes = base64.b64decode(b64_string)
    image_buf = io.BytesIO(image_bytes)
    img_ndarray = mpimg.imread(image_buf, format='JPG')
    return img_ndarray


def ndarray_to_tkinter_image(img_ndarray):
    f = io.BytesIO()
    imsave(f, img_ndarray, plugin="pil")
    out_img = io.BytesIO()
    out_img.write(f.getvalue())
    img_obj = Image.open(out_img)
    pixel_size = img_obj.size
    img_obj = resize_image(img_obj)
    tk_image = ImageTk.PhotoImage(img_obj)
    return tk_image, pixel_size


def resize_image(img_obj):
    # resize image but keep aspect ratio
    mywidth = 512
    wpercent = (mywidth / float(img_obj.size[0]))
    hsize = int((float(img_obj.size[1]) * float(wpercent)))
    img_obj = img_obj.resize((mywidth, hsize), PIL.Image.ANTIALIAS)
    return img_obj


def display_image(img_ndarray):
    try:
        plt.imshow(img_ndarray, interpolation="nearest")
        plt.show()
    except TypeError:
        return False
    return True


def create_filename(filename):
    new_filename = "images/{}".format(filename)
    found = True
    i = 0
    stem, ext = new_filename.split('.')
    while found is True:
        if i == 0:
            found = path.exists(new_filename)
        else:
            found = path.exists(stem + "_" + str(i) + "." + ext)
            new_filename = stem + "_" + str(i) + "." + ext
        i += 1
    return new_filename


def b64_to_image_file(b64, new_filename):
    image_bytes = base64.b64decode(b64)
    with open(new_filename, "wb") as out_file:
        out_file.write(image_bytes)
    return True


def upload_new_window():
    def upload_button():
        image_name = image_selection.get()
        image_entry.delete(0, 'end')
        b64_str = image_file_to_b64("images/{}".format(image_name))
        if b64_str is False:  # file not found
            not_found_message = "{} could not be found. \n" \
                                "Check image spelling and extension type " \
                                "and ensure image is in the /images " \
                                "directory".format(image_name)
            messagebox.showerror(title="File Not Found",
                                 message=not_found_message,
                                 icon="error")
            return
        elif not b64_str:  # not an image
            not_image_message = "{} is not a supported filetype. " \
                                "Please select an image.".format(image_name)
            messagebox.showerror(title="File Not Supported",
                                 message=not_image_message,
                                 icon="error")
            return
        else:
            upload_out = upload_image(image_name, b64_str)
            if upload_out is True:
                success_message = "Image uploaded successfully"
                messagebox.showinfo(title="Upload Success",
                                    message=success_message)
                sub_upload.destroy()
            else:
                messagebox.askretrycancel(title="Upload Failure",
                                          message=upload_out,
                                          icon="error")
        return

    def browse_button():
        filename = filedialog.askopenfilename(initialdir=os.getcwd() + "/images",
                                              parent=sub_upload,
                                              title='Select file',
                                              filetypes=(("JPG files", "*.jpg"),
                                                         ("JPEG files", "*.jpeg"),
                                                         ("PNG files", "*.png"),
                                                         ("All files", "*.*")))
        if filename is not None:
            print(filename)
            im_name = filename.split('/')
            im_name = im_name[-1]
            image_entry.delete(0, END)
            image_entry.insert(0, im_name)
            return im_name
        return

    def back_button():
        sub_upload.destroy()
        return

    sub_upload = Toplevel()  # sets up main window
    sub_upload.title("Upload New")
    sub_upload.columnconfigure(0, pad=8)
    sub_upload.columnconfigure(1, pad=8)
    sub_upload.columnconfigure(2, pad=8)
    sub_upload.rowconfigure(1, pad=5)

    # Add main label
    top_label = ttk.Label(sub_upload, text="Upload New",
                          font='Helvetica 10 bold')
    top_label.grid(column=0, row=0, columnspan=2, sticky=W)

    # Image selection
    select_label = ttk.Label(sub_upload, text="Choose an image:")
    select_label.grid(column=0, row=1)
    image_selection = StringVar()
    image_entry = ttk.Entry(sub_upload, textvariable=image_selection, width=30)
    image_entry.grid(column=1, row=1)

    # Add buttons
    browse_btn = ttk.Button(sub_upload, text="Browse", command=browse_button)
    browse_btn.grid(column=2, row=1)
    upload_btn = ttk.Button(sub_upload, text="Upload", command=upload_button)
    upload_btn.grid(column=1, row=2)
    back_btn = ttk.Button(sub_upload, text="Back", command=back_button)
    back_btn.grid(column=2, row=2, columnspan=2)

    return


def image_file_to_b64(filename):
    try:
        with open(filename, "rb") as image_file:
            b64_bytes = base64.b64encode(image_file.read())
        b64_str = str(b64_bytes, encoding='utf-8')
        return b64_str
    except IOError:  # file not found
        return False


def upload_image(image_name, b64_str):
    new_image = {"image": image_name, "b64_string": b64_str}
    r = requests.post(server_name + "/api/upload_image", json=new_image)
    if r.status_code != 200:
        failure_message = "Image upload failed: {} - {}" \
            .format(r.status_code, r.text)
        return failure_message
    else:
        return True


def display_window(tk_image, size, image):
    def back_button():
        sub_disp.destroy()
        return

    def update_list_combobox():
        image_list = get_image_list()
        image_choice_box['values'] = image_list

    def details_button():
        time = get_details(image)
        deets_message = create_deets_message(time, size, image)
        messagebox.showinfo(title="Image Details",
                            message=deets_message)
        return

    def compare_button():
        if image_choice.get() == "":
            no_selection_message = "Please select an image to " \
                                   "compare with."
            messagebox.showerror(title="Selection Error",
                                 message=no_selection_message,
                                 icon="error")
        else:
            b64_to_convert = fetch_b64(image_choice.get())
            try:
                nd_to_disp = b64_string_to_ndarray(b64_to_convert)
            except binascii.Error:
                messagebox.askretrycancel(title="Failure to Find Image",
                                          message=b64_to_convert,
                                          icon="error")
                return
            tk_image2, pixel_size = ndarray_to_tkinter_image(nd_to_disp)
            compare_window(image, tk_image, image_choice.get(), tk_image2)
        return

    sub_disp = Toplevel()  # sets up main window
    sub_disp.title("Display")
    sub_disp.columnconfigure(0, pad=8)
    sub_disp.columnconfigure(1, pad=8)
    sub_disp.columnconfigure(2, pad=8)
    sub_disp.columnconfigure(3, pad=8)

    # Add main label
    top_label = ttk.Label(sub_disp, text="{}".format(image),
                          font='Helvetica 10 bold')
    top_label.grid(column=1, row=0, columnspan=2)

    image_label = ttk.Label(sub_disp, image=tk_image)
    image_label.image = tk_image
    image_label.grid(column=0, row=1, columnspan=4)

    # Add buttons
    compare_btn = ttk.Button(sub_disp, text="Compare", command=compare_button)
    compare_btn.grid(column=0, row=3)
    deets_btn = ttk.Button(sub_disp, text="Details", command=details_button)
    deets_btn.grid(column=2, row=3)
    back_btn = ttk.Button(sub_disp, text="Back", command=back_button)
    back_btn.grid(column=3, row=3)

    # Image selection
    select_label = ttk.Label(sub_disp, text="Select:")
    select_label.grid(column=0, row=2)
    image_choice = StringVar()
    image_choice_box = ttk.Combobox(sub_disp, textvariable=image_choice,
                                    postcommand=update_list_combobox)
    image_choice_box.grid(column=1, row=2)
    image_choice_box.state(["readonly"])

    return


def get_details(image_name):
    r = requests.get(server_name + "/api/get_details/{}".format(image_name))
    if r.status_code != 200:
        failure_message = "Detail collection failed: {} - {}" \
            .format(r.status_code, r.text)
        return failure_message
    else:
        return json.loads(r.text)


def create_deets_message(time, size, image):
    if "inverted" in image:
        time_type = "processed"
    else:
        time_type = "uploaded"
    width, height = size
    deets_message = "Time {}: {}\n" \
                    "Image size: {} x {}" \
        .format(time_type, time, width, height)
    return deets_message


def compare_window(name1, tk_image1, name2, tk_image2):
    def back_button():
        sub_comp.destroy()
        return

    sub_comp = Toplevel()  # sets up main window
    sub_comp.title("Compare")
    sub_comp.columnconfigure(0, pad=8)
    sub_comp.columnconfigure(1, pad=8)
    sub_comp.columnconfigure(2, pad=8)
    sub_comp.columnconfigure(3, pad=8)

    # Top Labels
    top_label1 = ttk.Label(sub_comp, text="{}".format(name1),
                           font='Helvetica 10 bold')
    top_label1.grid(column=0, row=0, columnspan=2)
    top_label2 = ttk.Label(sub_comp, text="{}".format(name2),
                           font='Helvetica 10 bold')
    top_label2.grid(column=2, row=0, columnspan=2)

    # Images
    image_label = ttk.Label(sub_comp, image=tk_image1)
    image_label.image = tk_image1
    image_label.grid(column=0, row=1, columnspan=2)
    image_label2 = ttk.Label(sub_comp, image=tk_image2)
    image_label2.image = tk_image2
    image_label2.grid(column=2, row=1, columnspan=2)

    # Add buttons
    back_btn = ttk.Button(sub_comp, text="Back", command=back_button)
    back_btn.grid(column=1, row=3, columnspan=2)

    return


if __name__ == "__main__":
    main_window()
