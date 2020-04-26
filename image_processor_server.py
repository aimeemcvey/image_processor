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
    """Adds new image to the image database via name
    When a post request is made to /api/upload_image, the input
    must be validated and checked to confirm the image isn't
    already in the database before the image name, corresponding
    b64 string, and upload time are added to the image database.
    Args:
        None
    Returns:
        str: results of post request
        int: HTTP status code
    """
    in_dict = request.get_json()
    check_result = verify_image_info(in_dict)
    if check_result is not True:
        return check_result, 400
    if is_image_in_database(in_dict["image"]) is True:
        return "Image {} has already been added to server" \
                   .format(in_dict["image"]), 400
    # check if inverted form of image in db
    if "inverted" in in_dict["image"]:
        image_name = return_name(in_dict["image"])
        if is_image_in_database(image_name) is True:
            return "Image {} is already on server under {} entry" \
                   .format(in_dict["image"], image_name), 400
    add_image_to_db(in_dict)
    return "Image added", 200


def verify_image_info(in_dict):
    """Verifies post request was made with correct format
    The input dictionary must have the appropriate data keys
    and types, or be convertible to correct types, to be added
    to the image database.
    Args:
        in_dict (dict): input with image name and b64 str
    Returns:
        str: if error, returns error message
        bool: if input verified, returns True
    """
    expected_keys = ("image", "b64_string")
    expected_types = (str, str)
    for i, key in enumerate(expected_keys):
        if key not in in_dict.keys():
            return "{} key not found".format(key)
        if type(in_dict[key]) is not expected_types[i]:
            return "{} value not a string".format(key)
    return True


def is_image_in_database(name):
    """Checks if image has previously been added to database
    To be added to the image database, the image must not
    previously have been added to the database.
    Args:
        name (str): image name
    Returns:
        bool: if name in database, True; if not, False
    """
    check_db = []
    db_items = Image.objects.raw({})
    for item in db_items:
        check_db.append(item.image_name)
    if name in check_db:
        return True
    return False


def add_image_to_db(in_dict):
    """Adds new image to image database list via image name
    The image name, corresponding b64 str, and upload timestamp
    are added to the image database to maintain proper,
    permanent record of uploaded images.
    Args:
        in_dict (dict): input with image name and b64 str
    Returns:
        str: image name the data was saved under in database
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_image = Image(image_name=in_dict["image"],
                      image_formats={"b64_str": in_dict["b64_string"]},
                      upload_time=timestamp)
    new_image.save()
    logging.info("Image {} added to database".format(in_dict["image"]))
    return new_image.image_name


@app.route("/api/image_list", methods=["GET"])
def get_image_list_from_db():
    """Returns list of images in database
    If requested, all recorded images (original and processed)
    saved on the database are returned. An image can then be
    selected to display or download.
    Args:
        None
    Returns:
        list: all stored images
        int: HTTP status code
    """
    im_list = generate_image_list()
    return jsonify(im_list), 200


def generate_image_list():
    """Generates list of all images stored in database
    The list of images are provided for the user to choose
    from to perform selected actions upon, including
    display and download.
    Args:
        None
    Returns:
        list: sorted list of all images stored in database
    """
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
    """Inverts image and adds to the image database via name
    When a post request is made to /api/invert_image, the input
    must be validated and checked to confirm the image is
    already in the database before the image is inverted and
    stored under the original image name.
    Args:
        None
    Returns:
        str: results of post request; b64 str if success
        int: HTTP status code
    """
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
    """Verifies post request was made with correct format
    The input dictionary must have the appropriate data keys
    and types, or be convertible to correct types, to be added
    to the image database.
    Args:
        in_dict (dict): input with image name
    Returns:
        str: if error, returns error message
        bool: if input verified, returns True
    """
    expected_key = "image"
    expected_type = str
    if expected_key not in in_dict.keys():
        return "{} key not found".format(expected_key)
    if type(in_dict[expected_key]) is not expected_type:
        return "{} value not a string".format(expected_key)
    return True


def is_inverted_in_database(name):
    """Checks if image has previously been inverted
    To be inverted and added to the image database, the image
    must not previously have been inverted and added.
    Args:
        name (str): image name
    Returns:
        bool: if name in database, True; if not, False
    """
    db_item = Image.objects.raw({"_id": name})
    pt = None
    for item in db_item:
        pt = item.processed_time
    if pt is None:
        return False
    return True


def locate_b64_string(im_name, which="orig"):
    """Locates b64 str corresponding to image name and status
    The b64 string was stored under the image name. To invert
    or display the image, the b64 str is needed for conversion
    to the proper data type. The b64 string can be located for
    the original or inverted image.
    Args:
        im_name (str): image name
        which (str): status of image (default "orig)
    Returns:
        str: b64 str corresponding to image
    """
    to_act = Image.objects.raw({"_id": im_name})
    for doc in to_act:
        format_dict = doc.image_formats
        if which is "orig":
            b64_str_to_use = format_dict["b64_str"]
        elif which is "inverted":
            b64_str_to_use = format_dict["inverted_b64_str"]
    return b64_str_to_use


def b64_string_to_ndarray(b64_string):
    """Converts image b64 string to ndarray
    The image must be in the ndarray format for inversion.
    Args:
        b64_string (str): image in b64 str format
    Returns:
        numpy.ndarray: image in ndarray format
    """
    image_bytes = base64.b64decode(b64_string)
    image_buf = io.BytesIO(image_bytes)
    img_ndarray = mpimg.imread(image_buf, format='JPG')
    return img_ndarray


def process_image_inversion(ndarray):
    """Inverts ndarray to invert image
    The image must be in the ndarray format for inversion.
    This ndarray can then be inverted to obtain an ndarray
    that can further be converted into a b64 str and
    displayable image.
    Args:
        ndarray (numpy.ndarray): image in ndarray format
    Returns:
        numpy.ndarray: inverted image in ndarray format
    """
    inverted_nd = util.invert(ndarray)
    return inverted_nd


def ndarray_to_b64_string(img_ndarray):
    """Converts image ndarray to b64 str
    The image must be in the b64 str format to be
    added to the database and sent to the client.
    Args:
        img_ndarray (numpy.ndarray): image in ndarray format
    Returns:
        str: image in b64 str format
    """
    f = io.BytesIO()
    imsave(f, img_ndarray, plugin='pil')
    y = base64.b64encode(f.getvalue())
    b64_string = str(y, encoding='utf-8')
    return b64_string


def add_inverted_image_to_db(b64_str, name):
    """Adds inverted image to image database list via image name
    The inverted image's b64 str and processing timestamp
    are added to the image database under the original image
    name to maintain proper, permanent record of uploaded images.
    Args:
        b64_str (str): b64 str to be added to database
        name (str): image name under which the str added
    Returns:
        str: image name the data was saved under in database
    """
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
    """Obtains and returns b64 str corresponding to image name
    When a get request is made, the input must be validated
    before the corresponding b64 str is collected from the
    database and returned to the client. Both original and
    inverted image requests are accommodated. Only images
    present in the database are available for client selection.
    Args:
        image_name (str): image for which b64 str requested
    Returns:
        str: results of post request; b64 str if success
        int: HTTP status code
    """
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
    """Converts inverted image name to original name
    Inverted images are stored in the database under the image
    they're derived from. As such, to locate information
    corresponding to the inverted image, the database must
    be queried via the original image name.
    Args:
        image_name (str): inverted image name
    Returns:
        str: original image name
    """
    whole_stem, ext = image_name.split('.')
    stem, inv = whole_stem.split('_')
    image_name = stem + "." + ext
    return image_name


def verify_name_input(image):
    """Verifies get request was made with correct format
    The input name in the get URL must have the appropriate data
    type and correspond to an image in the database to locate
    corresponding information.
    Args:
        image (str): image name
    Returns:
        str: if error, returns error message
        bool: if input verified, returns True
    """
    if type(image) is not str:
        return "Bad image name in URL"
    if is_image_in_database(image) is False:
        return "Image {} does not exist in database".format(image)
    return True


@app.route("/api/get_details/<image_name>", methods=["GET"])
def get_im_details(image_name):
    """Obtains and returns details corresponding to image name
    When a get request is made, the input must be validated
    before the corresponding details are collected from the
    database and returned to the client. Both original and
    inverted image requests are accommodated. Only images
    present in the database are available for client selection.
    Args:
        image_name (str): image for which b64 str requested
    Returns:
        str: results of post request
        int: HTTP status code
    """
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
    """Locates details corresponding to image name and status
    Image details were stored under the image name. Details can
    be located for the original or inverted image. If the image
    is original, the upload time is returned. If the image is
    inverted, the processed time is returned.
    Args:
        im_name (str): image name
        which (str): status of image (default "orig)
    Returns:
        str: upload or processed time of image
    """
    to_act = Image.objects.raw({"_id": im_name})
    for doc in to_act:
        if which is "orig":
            im_deets = doc.upload_time
        elif which is "inverted":
            im_deets = doc.processed_time
    return im_deets


if __name__ == "__main__":
    app.run()
