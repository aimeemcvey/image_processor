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


def test_locate_b64_string():
    from image_processor_server import locate_b64_string
    in_dict = {'image': 'acl100.jpg'}
    answer = locate_b64_string(in_dict)
    expected = "3lkewar90eq3ljafjdl"
    assert answer == expected

#
#
# def b64_string_to_ndarray(b64_string):
#     image_bytes = base64.b64decode(b64_string)
#     image_buf = io.BytesIO(image_bytes)
#     # check jpg and png differences
#     img_ndarray = mpimg.imread(image_buf, format='JPG')
#     return img_ndarray
#
#
# def process_image_inversion(ndarray):
#     inverted_nd = util.invert(ndarray)
#     return inverted_nd
#
#
# def ndarray_to_b64_string(img_ndarray):
#     f = io.BytesIO()
#     imsave(f, img_ndarray, plugin='pil')
#     y = base64.b64encode(f.getvalue())
#     b64_string = str(y, encoding='utf-8')
#     return b64_string
