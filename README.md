# Image Processor [![Build Status](https://travis-ci.com/BME547-Spring2020/final-project-aimeemcvey.svg?token=uYZMqDdwHppZCbLZESzP&branch=master)](https://travis-ci.com/BME547-Spring2020/final-project-aimeemcvey)
This project is an image processor that allows uploading of images to a web-server, stores those uploaded images in a database, allows performing image-processing tasks on the web-server, and also permits displaying, downloading, and comparing the original and processed images.

## Server
The server is located at **vcm-13874.vm.duke.edu:5000**. It is NOT currently running to save resources.

## Instructions
A demo showcasing use of the GUI client can be viewed in the `Image_Processor_Demo.mp4` file.

To run the GUI client, input `image_processor_client.py` in a bash window. The GUI client presents a drop-down box housing the available images on the server. Any of these images can be selected and acted upon. The options below the drop-down box allow the user to select whether to invert, display, or download the image. The `Ok` button will implement the selected option on the selected image. Each action must be confirmed by the user before implementation. The `Cancel` option closes the GUI window.

The  `Invert` action will invert the selected image for storage on the database. A confirmation message will be displayed upon success. The inverted image will then appear in the drop-down box for display or download.

The `Display` action will display the selected image in a new window. This window has a couple of options at the bottom. Selecting an image from the drop-down box and clicking `Compare` will allow you to compare the previously chosen image and the newly chosen image side-by-side. `Details` returns the image details, including the time the image was uploaded or processed (depending on if it's an original or processed image) and the image pixel size.

The `Download` action will download the selected image to your `\images` folder. If an image of the same name already exists in the folder, a number will be appended to the image name. Again, upon success, a confirmation message will be displayed.

If you wish to upload a new image, select the `Upload New` button. This will bring up a new window. Select `Browse` to find the image you wish to upload on your computer. Then select `Upload` to upload the image to the server. A confirmation message will be displayed upon success. Select `Back` to return to the main window.


## Overview
The server and GUI client are currently fully functional with the server running at the above address.

### GUI Client
The GUI client (`image_processor_client.py`) allows the following actions through issuing of RESTful API requests:
* Allows the user to select an image for upload to the server
  
* Allows the user to choose an uploaded image and conduct an image processing step (currently, inversion) on that image

* Ability to choose and display an image (original or processed) from the server

* Option to compare two images from the server side-by-side

* Option to display useful metadata of displayed images, including:
  + Timestamp when uploaded (or processed)
  + Image size (e.g., X x Y pixels)

* Option to download an image (original or processed) from the server and save it to the computer

### Cloud Server
The server (`image_processor_server.py`) is a cloud-based web service that implements the requests of the GUI client:

* Accepts images and their timestamp for uploading and storage in a persistent database (MongoDB)

* Conducts image processing methods on selected files and stores the processed images in the database
  with the timestamp of processing
  
* Communicates with and utilizes a persistent database that:
  + Stores uploaded images and timestamps
  + Stores processed images and timestamps

* Provides a list of available images to the client

* Provides for the downloading of an image from the database to the client
