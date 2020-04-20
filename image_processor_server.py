# image_processor_server.py
from flask import Flask, jsonify, request
import logging
from datetime import datetime
import requests
from pymodm import connect, MongoModel, fields

connect("mongodb+srv://db_access:swim4life@aimeemcv-7rfsl.mongodb.net/imagedb?retryWrites=true&w=majority")
app = Flask(__name__)


class Image(MongoModel):
    image_name = fields.CharField(primary_key=True)
    image_formats = fields.ListField(field=fields.DictField())
    upload_time = fields.DateTimeField
    image_size = fields.ListField(field=fields.DictField())
    processed_info = fields.ListField(field=fields.DictField())


@app.route("/api/upload_image", methods=["POST"])
def post_new_image():
    in_dict = request.get_json()
    check_result = verify_image_info(in_dict)
    if check_result is not True:
        return check_result, 400
    # if is_image_in_database(in_dict["image_name"]) is True:
    #     return "Image {} has already been added to server" \
    #                .format(in_dict["image_name"]), 400
    # add_image_to_db(in_dict["image_name"])
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


if __name__ == "__main__":
    app.run()
