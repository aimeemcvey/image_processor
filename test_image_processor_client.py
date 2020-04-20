# test_image_processor_client.py
import pytest


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
