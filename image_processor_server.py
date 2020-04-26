# image_processor_server.py
from flask import Flask, jsonify, request
import logging
from datetime import datetime
import requests
from pymodm import connect, MongoModel, fields
from pymodm import errors as pymodm_errors
import base64
import io
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from skimage.io import imsave
from skimage import util

connect("mongodb+srv://db_access:swim4life@aimeemcv-7rfsl.mongodb.net/"
        "imagedb?retryWrites=true&w=majority")
app = Flask(__name__)
logging.basicConfig(filename="processor_info.log", filemode="w",
                    level=logging.INFO)


class Image(MongoModel):
    image_name = fields.CharField(primary_key=True)
    image_formats = fields.DictField()
    upload_time = fields.CharField()
    processed_time = fields.CharField()


@app.route("/api/upload_image", methods=["POST"])
def post_new_image():
    in_dict = request.get_json()
    check_result = verify_image_info(in_dict)
    if check_result is not True:
        return check_result, 400
    if is_image_in_database(in_dict["image"]) is True:
        return "Image {} has already been added to server" \
                   .format(in_dict["image"]), 400
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


def is_image_in_database(name):
    check_db = []
    db_items = Image.objects.raw({})
    for item in db_items:
        check_db.append(item.image_name)
    if name in check_db:
        return True
    return False


def add_image_to_db(in_dict):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_image = Image(image_name=in_dict["image"],
                      image_formats={"b64_str": in_dict["b64_string"]},
                      upload_time=timestamp)
    new_image.save()
    logging.info("Image {} added to database".format(in_dict["image"]))
    return new_image.image_name


@app.route("/api/image_list", methods=["GET"])
def get_image_list_from_db():
    im_list = generate_image_list()
    return jsonify(im_list), 200


def generate_image_list():
    image_list = []  # if no images in db, list will be empty
    db_items = Image.objects.raw({})
    for item in db_items:
        image_list.append(item.image_name)
        if is_inverted_in_database(item.image_name) is True:
            stem, ext = item.image_name.split('.')
            inverted_name = stem + "_inverted." + ext
            image_list.append(inverted_name)
    image_list.sort()
    return image_list


@app.route("/api/invert_image", methods=["POST"])
def post_invert_image():
    in_dict = request.get_json()
    check_result = verify_image_name(in_dict)
    if check_result is not True:
        return check_result, 400
    if is_image_in_database(in_dict["image"]) is False:
        return "Image {} not found in database" \
                   .format(in_dict["image"]), 400
    if is_inverted_in_database(in_dict["image"]) is True:
        return "Image {} has already been inverted" \
                   .format(in_dict["image"]), 400
    b64_str_to_invert = locate_b64_string(in_dict["image"])
    ndarray_to_invert = b64_string_to_ndarray(b64_str_to_invert)
    inverted_nd = process_image_inversion(ndarray_to_invert)
    inverted_b64 = ndarray_to_b64_string(inverted_nd)
    add_inverted_image_to_db(inverted_b64, in_dict["image"])
    return inverted_b64, 200


def verify_image_name(in_dict):
    expected_key = "image"
    expected_type = str
    if expected_key not in in_dict.keys():
        return "{} key not found".format(expected_key)
    if type(in_dict[expected_key]) is not expected_type:
        return "{} value not a string".format(expected_key)
    return True


def is_inverted_in_database(name):
    db_item = Image.objects.raw({"_id": name})
    pt = None
    for item in db_item:
        pt = item.processed_time
    if pt is None:
        return False
    return True


def locate_b64_string(im_name, which="orig"):
    to_act = Image.objects.raw({"_id": im_name})
    for doc in to_act:
        format_dict = doc.image_formats
        if which is "orig":
            b64_str_to_use = format_dict["b64_str"]
        elif which is "inverted":
            b64_str_to_use = format_dict["inverted_b64_str"]
    return b64_str_to_use


def b64_string_to_ndarray(b64_string):
    image_bytes = base64.b64decode(b64_string)
    image_buf = io.BytesIO(image_bytes)
    img_ndarray = mpimg.imread(image_buf, format='JPG')
    return img_ndarray


def process_image_inversion(ndarray):
    inverted_nd = util.invert(ndarray)
    return inverted_nd


def ndarray_to_b64_string(img_ndarray):
    f = io.BytesIO()
    imsave(f, img_ndarray, plugin='pil')
    y = base64.b64encode(f.getvalue())
    b64_string = str(y, encoding='utf-8')
    return b64_string


def add_inverted_image_to_db(b64_str, name):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_add = Image.objects.raw({"_id": name})
    for doc in to_add:
        doc.processed_time = timestamp
        doc.image_formats.update({"inverted_b64_str": b64_str})
        doc.save()
    logging.info("Image {} inverted and added to database".format(name))
    return doc.image_name


@app.route("/api/fetch_b64/<image_name>", methods=["GET"])
def get_b64_from_db(image_name):
    status = "og"
    if "inverted" in image_name:
        image_name = return_name(image_name)
        status = "inv"
    check_result = verify_name_input(image_name)
    if check_result is not True:
        return check_result, 400
    if status is "inv":
        b64_to_disp = locate_b64_string(image_name, "inverted")
        logging.info("Image {} inverted b64 string "
                     "returned".format(image_name))
    else:
        b64_to_disp = locate_b64_string(image_name)
        logging.info("Image {} b64 string returned".format(image_name))
    return jsonify(b64_to_disp), 200


def return_name(image_name):
    whole_stem, ext = image_name.split('.')
    stem, inv = whole_stem.split('_')
    image_name = stem + "." + ext
    return image_name


def verify_name_input(image):
    if type(image) is not str:
        return "Bad image name in URL"
    if is_image_in_database(image) is False:
        return "Image {} does not exist in database".format(image)
    return True


@app.route("/api/get_details/<image_name>", methods=["GET"])
def get_im_details(image_name):
    status = "og"
    if "inverted" in image_name:
        image_name = return_name(image_name)
        status = "inv"
    check_result = verify_name_input(image_name)
    if check_result is not True:
        return check_result, 400
    if status is "inv":
        im_details = locate_details(image_name, "inverted")
        logging.info("Image {} inverted details returned".format(image_name))
    else:
        im_details = locate_details(image_name)
        logging.info("Image {} details returned".format(image_name))
    return jsonify(im_details), 200


def locate_details(im_name, which="orig"):
    to_act = Image.objects.raw({"_id": im_name})
    for doc in to_act:
        if which is "orig":
            im_deets = doc.upload_time
        elif which is "inverted":
            im_deets = doc.processed_time
    return im_deets


if __name__ == "__main__":
    app.run()
