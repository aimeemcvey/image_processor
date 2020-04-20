# image_processor_server.py
from flask import Flask, jsonify, request
import logging
from datetime import datetime
import requests
from pymodm import connect, MongoModel, fields
from PIL import Image, ImageTk
import base64
import io
import matplotlib.image as mpimg
from skimage.io import imsave

connect("mongodb+srv://db_access:swim4life@aimeemcv-7rfsl.mongodb.net/"
        "imagedb?retryWrites=true&w=majority")
app = Flask(__name__)


class Image(MongoModel):
    image_name = fields.CharField(primary_key=True)
    image_formats = fields.DictField()
    upload_time = fields.CharField()
    # image_size = fields.ListField()
    # processed_info = fields.ListField()


@app.route("/api/upload_image", methods=["POST"])
def post_new_image():
    in_dict = request.get_json()
    check_result = verify_image_info(in_dict)
    if check_result is not True:
        return check_result, 400
    # if is_image_in_database(in_dict["image_name"]) is True:
    #     return "Image {} has already been added to server" \
    #                .format(in_dict["image_name"]), 400
    add_image_to_db(in_dict)
    return "Image added", 200


def verify_image_info(in_dict):
    expected_keys = ("image", "b64_string")
    expected_types = (str, str)
    for i, key in enumerate(expected_keys):
        if key not in in_dict.keys():
            return "{} key not found".format(key)
        if type(in_dict[key]) is not expected_types[i]:
            return "{} value not a string".format(key)
    return True


def b64_string_to_ndarray(b64_string):
    image_bytes = base64.b64decode(b64_string)
    image_buf = io.BytesIO(image_bytes)
    # check jpg and png differences
    img_ndarray = mpimg.imread(image_buf, format='JPG')
    return img_ndarray


def add_image_to_db(in_dict):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_image = Image(image_name=in_dict["image"],
                      image_formats={"b64_str": in_dict["b64_string"]},
                      upload_time=timestamp)
    new_image.save()
    return True


if __name__ == "__main__":
    app.run()
