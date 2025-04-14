import os
from flask import Blueprint, jsonify, request

from services.upload_image import *

upload_image_bp = Blueprint("upload_image", __name__)


@upload_image_bp.route("/upload-image", methods=["POST"])
def upload_image():
    """
    Endpoint para upload de imagem.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    detected, detected_names = call_facial_recog(image)

    if detected:
        message = "Face(s) detected!"
    else:
        message = "No face detected!"
    
    response = {
        "message": message,
        "detected": detected,
        "detected_names": detected_names
    }

    print(response)

    return jsonify(response), 200
