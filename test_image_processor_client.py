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
#
#
# def display_image(img_ndarray):
#     try:
#         plt.imshow(img_ndarray, interpolation="nearest")
#         plt.show()
#     except Error:
#         return False
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
