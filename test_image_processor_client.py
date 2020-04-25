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
#
#
# def b64_to_image_file(b64, new_filename):
#     image_bytes = base64.b64decode(b64)
#     with open(new_filename, "wb") as out_file:
#         out_file.write(image_bytes)
#     return True


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
