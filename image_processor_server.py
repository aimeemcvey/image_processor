# image_processor_server.py
from flask import Flask, jsonify, request
import logging
from datetime import datetime
import requests
from pymodm import connect, MongoModel, fields
from PIL import Image, ImageTk
import base64
import io

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
    # verify it's actually an image w correct extension and route
    # if is_image_in_database(in_dict["image_name"]) is True:
    #     return "Image {} has already been added to server" \
    #                .format(in_dict["image_name"]), 400
    b64_str = image_file_to_b64("images/{}".format(in_dict["image"]))
    in_dict["b64_string"] = b64_str
    # make sure in right directory - error message
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


def image_file_to_b64(filename):
    print(filename)
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_str = str(b64_bytes, encoding='utf-8')
    return b64_str


def add_image_to_db(in_dict):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_image = Image(image_name=in_dict["image"],
                      image_formats={"b64_str": in_dict["b64_string"]},
                      upload_time=timestamp)
    new_image.save()
    return True


if __name__ == "__main__":
    app.run()
