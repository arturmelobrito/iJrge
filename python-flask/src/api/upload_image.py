import os
from flask import Blueprint, jsonify, request

from services.upload_image import save_image

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

    save_image(image)

    return jsonify({"message": f"Image {image.filename} uploaded successfully!"}), 200
