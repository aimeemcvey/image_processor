# test_image_processor_server.py
import pytest


@pytest.mark.parametrize("in_dict, expected", [
    ({"image": "acl100.jpg", "b64_string": ""}, True),
    ({"imge": "acl100.jpg", "b64_string": ""}, "image key not found"),
    ({"image": "acl100.jpg", "b64_string": 673241},
     "b64_string value not a string"),
])
def test_verify_image_info(in_dict, expected):
    from image_processor_server import verify_image_info
    answer = verify_image_info(in_dict)
    assert answer == expected


def test_is_image_in_database_true():
    from image_processor_server import is_image_in_database
    answer = is_image_in_database("acl100.jpg")
    expected = True
    assert answer == expected


def test_is_image_in_database_false():
    from image_processor_server import is_image_in_database
    answer = is_image_in_database("acl99.jpg")
    expected = False
    assert answer == expected


def test_add_image_to_db():
    from image_processor_server import add_image_to_db
    in_dict = {'image': 'acl100.jpg', 'b64_string': "3lkewar90eq3ljafjdl"}
    answer = add_image_to_db(in_dict)
    expected = 'acl100.jpg'
    assert answer == expected


def test_add_image_to_db_another():
    from image_processor_server import add_image_to_db
    in_dict = {'image': 'acl200.jpg', 'b64_string': "8dasfdljk324098dsajl"}
    answer = add_image_to_db(in_dict)
    expected = 'acl200.jpg'
    assert answer == expected


def test_generate_image_list():
    from image_processor_server import generate_image_list
    answer = generate_image_list()
    expected = ['acl100.jpg', 'acl200.jpg']
    assert answer == expected


@pytest.mark.parametrize("in_dict, expected", [
    ({"image": "acl100.jpg"}, True),
    ({"imge": "acl100.jpg"}, "image key not found"),
    ({"image": 100}, "image value not a string"),
])
def test_verify_image_name(in_dict, expected):
    from image_processor_server import verify_image_name
    answer = verify_image_name(in_dict)
    assert answer == expected


def test_add_inverted_image_to_db():
    from image_processor_server import add_inverted_image_to_db
    answer = add_inverted_image_to_db("904j5alkfsd0943ld", 'acl100.jpg')
    expected = 'acl100.jpg'
    assert answer == expected


def test_is_inverted_in_database_true():
    from image_processor_server import is_inverted_in_database
    answer = is_inverted_in_database("acl100.jpg")
    expected = True
    assert answer == expected


def test_is_inverted_in_database_false():
    from image_processor_server import is_inverted_in_database
    answer = is_inverted_in_database("acl200.jpg")
    expected = False
    assert answer == expected


def test_locate_b64_string():
    from image_processor_server import locate_b64_string
    in_dict = {'image': 'acl100.jpg'}
    answer = locate_b64_string(in_dict)
    expected = "3lkewar90eq3ljafjdl"
    assert answer == expected


def test_b64_string_to_ndarray():
    from image_processor_client import image_file_to_b64
    from image_processor_server import b64_string_to_ndarray
    b64 = image_file_to_b64("images/acl1_test.jpg")
    nd = b64_string_to_ndarray(b64)
    answer = nd[25][0:5]
    expected = [[5, 5, 5],
                [5, 5, 5],
                [5, 5, 5],
                [5, 5, 5],
                [5, 5, 5]]
    assert (answer == expected).all


def test_process_image_inversion():
    from image_processor_client import image_file_to_b64
    from image_processor_server import b64_string_to_ndarray
    from image_processor_server import process_image_inversion
    b64 = image_file_to_b64("images/acl1_test.jpg")
    nd = b64_string_to_ndarray(b64)
    inverted_nd = process_image_inversion(nd)
    answer = inverted_nd[25][0:5]
    expected = [[5, 5, 5],
                [5, 5, 5],
                [5, 5, 5],
                [5, 5, 5],
                [5, 5, 5]]
    assert (answer == expected).all


def test_ndarray_to_b64_string():
    from image_processor_client import image_file_to_b64
    from image_processor_server import b64_string_to_ndarray
    from image_processor_server import ndarray_to_b64_string
    b64 = image_file_to_b64("images/acl2_test.jpg")
    nd = b64_string_to_ndarray(b64)
    answer = ndarray_to_b64_string(nd)
    expected = 'iVBORw0KGgoAAAANSUhE'
    assert answer[0:20] == expected


@pytest.mark.parametrize("im_name, expected", [
    ("acl100.jpg", True),
    (39032410, "Bad image name in URL"),
    ("acl3.jpg", "Image acl3.jpg does not exist in database"),
])
def test_verify_name_input(im_name, expected):
    from image_processor_server import verify_name_input
    answer = verify_name_input(im_name)
    assert answer == expected
