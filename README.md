# Image Processor [![Build Status](https://travis-ci.com/BME547-Spring2020/final-project-aimeemcvey.svg?token=uYZMqDdwHppZCbLZESzP&branch=master)](https://travis-ci.com/BME547-Spring2020/final-project-aimeemcvey)
This project is an image processor that allows uploading of images to a web-server, stores those uploaded images in a database, allows performing image-processing tasks on the web-server, and also permits displaying, downloading, and comparing the original and processed images.

## Server
The server is running at **vcm-13874.vm.duke.edu:5000**.

## Instructions
demo can be seen xxx

## Overview
describe final performance and state of project

### GUI Client
The GUI client (image_processor_client.py) allows the following actions through issuing of RESTful API requests:
* Allows the user to select an image for upload to the server
  
* Allows the user to choose an uploaded image and conduct an image processing step (currently, inversion) on that image

* Ability to choose and display an image (original or processed) from the server

* Option to compare two images from the server side-by-side

* Option to display useful metadata of displayed images, including:
  + Timestamp when uploaded (or processed)
  + Image size (e.g., X x Y pixels)

* Option to download an image (original or processed) from the server and save it to the computer

### Cloud Server
The server is a cloud-based web service that implements the requests of the GUI client:

* Accepts images and their timestamp for uploading and storage in a persistent database (MongoDB)

* Conducts image processing methods on selected files and stores the processed images in the database
  with the timestamp of processing
  
* Communicates with and utilizes a persistent database that will:
  + Store uploaded images and timestamps
  + Store processed images and timestamps

* Provides a list of available images to the client

* Provides for the downloading of an image from the database to the client
