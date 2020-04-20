# test_image_processor_server.py
import pytest


@pytest.mark.parametrize("in_dict, expected", [
    ({"image": "acl1.jpg", "b64_string": ""}, True),
    ({"imge": "acl1.jpg", "b64_string": ""}, "image key not found"),
    ({"image": "acl1.jpg", "b64_string": 673241},
     "b64_string value not a string"),
])
def test_verify_image_info(in_dict, expected):
    from image_processor_server import verify_image_info
    answer = verify_image_info(in_dict)
    assert answer == expected


def test_add_image_to_db():
    from image_processor_server import add_image_to_db
    in_dict = {'image': 'acl1.jpg', 'b64_string': "3lkewar90eq3ljafjdl"}
    answer = add_image_to_db(in_dict)
    expected = True
    assert answer == expected
