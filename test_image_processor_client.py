# test_image_processor_client.py
import pytest


def test_b64_string_to_ndarray():
    from image_processor_client import image_file_to_b64
    from image_processor_client import b64_string_to_ndarray
    b64 = image_file_to_b64("images/acl1_test.jpg")
    nd = b64_string_to_ndarray(b64)
    answer = nd[25][0:5]
    expected = [[5, 5, 5],
                [5, 5, 5],
                [5, 5, 5],
                [5, 5, 5],
                [5, 5, 5]]
    assert (answer == expected).all


def test_ndarray_to_tkinter_image():
    from image_processor_client import image_file_to_b64
    from image_processor_client import b64_string_to_ndarray
    from image_processor_client import ndarray_to_tkinter_image
    from PIL import Image, ImageTk
    from tkinter import Tk
    test = Tk()
    b64 = image_file_to_b64("images/acl2_test.jpg")
    nd = b64_string_to_ndarray(b64)
    ans1, ans2 = ndarray_to_tkinter_image(nd)
    test.destroy()
    expected = 512, 512
    assert ans2 == expected


def test_display_image():
    from image_processor_client import image_file_to_b64
    from image_processor_client import b64_string_to_ndarray
    from image_processor_client import display_image
    b64 = image_file_to_b64("images/acl1_test.jpg")
    nd_array = b64_string_to_ndarray(b64)
    answer = display_image(nd_array)
    expected = True
    assert answer == expected


def test_create_filename():
    from image_processor_client import create_filename
    answer = create_filename("acl1.jpg")
    expected = "images/acl1_1.jpg"
    assert answer == expected


def test_b64_to_image_file():
    from image_processor_client import image_file_to_b64
    from image_processor_client import b64_to_image_file
    import filecmp
    import os
    b64str = image_file_to_b64("images/acl1_test.jpg")
    b64_to_image_file(b64str, "images/test_output.jpg")
    answer = filecmp.cmp("images/acl1_test.jpg",
                         "images/test_output.jpg")
    os.remove("images/test_output.jpg")
    expected = True
    assert answer == expected


def test_image_file_to_b64_exists():
    from image_processor_client import image_file_to_b64
    answer = image_file_to_b64("images/acl1.jpg")
    assert answer[0:20] == "/9j/4AAQSkZJRgABAgAA"


def test_image_file_to_b64_notfound():
    from image_processor_client import image_file_to_b64
    answer = image_file_to_b64("images/acl.jpg")
    expected = False
    assert answer == expected


def test_image_file_to_b64_wrongfiletype():
    from image_processor_client import image_file_to_b64
    answer = image_file_to_b64("images/test.txt")
    expected = ""
    assert answer == expected


def test_create_deets_message():
    from image_processor_client import create_deets_message
    answer = create_deets_message("2020-04-24 00:38:15",
                                  ("512", "512"), "acl2_inverted.jpg")
    expected = "Time processed: 2020-04-24 00:38:15\n" \
               "Image size: 512 x 512"
    assert answer == expected
