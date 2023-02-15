import json
import logging
import base64
from flask import Flask, jsonify, request
from product_finder import find_objects_and_query_catalog

application = Flask(__name__)

application.logger.setLevel(logging.INFO)

@application.route("/")
@application.route("/status")
def status():
    return jsonify({"status": "ok"})

@application.route("/predictions/json", methods=["POST"])
def create_prediction_json():
    data = request.data or "{}"
    body = json.loads(data)
    base64img = body.get("image")
    img_bytes = base64.decodebytes(base64img.encode())
    return jsonify(find_objects_and_query_catalog(img_bytes))

@application.route("/predictions/base64", methods=["POST"])
def create_prediction_base64():
    data = request.data
    img_bytes = base64.decodebytes(data)
    return jsonify(find_objects_and_query_catalog(img_bytes))

@application.route("/predictions/mp", methods=["POST"])
def create_prediction_mp():
    data = request.files['image']
    img_bytes = data.read()
    return jsonify(find_objects_and_query_catalog(img_bytes))

@application.route("/predictions/raw", methods=["POST"])
def create_prediction_raw():
    data = request.data
    return jsonify(find_objects_and_query_catalog(data))

def create_app():
   return application
