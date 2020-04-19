# image_processor_server.py
from flask import Flask, jsonify, request
import logging
from datetime import datetime
import requests

app = Flask(__name__)


