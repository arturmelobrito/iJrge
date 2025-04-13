from flask import Blueprint, request, jsonify
from services.face import FaceDetectionService

face_bp = Blueprint("face", __name__)
face_service = FaceDetectionService()


@face_bp.route("/detect", methods=["POST"])
def detect_face():
    """
    Endpoint para detectar faces em uma imagem enviada.

    A imagem deve ser enviada como um arquivo no form-data com a chave 'image'.

    Returns:
        JSON com o resultado da detecção.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image provided", "status": "error"}), 400

    image_file = request.files["image"]
    image_file.save("nova_imagem.jpg")

    if image_file.filename == "":
        return jsonify({"error": "No image selected", "status": "error"}), 400

    # Ler o conteúdo da imagem
    image_data = image_file.read()

    # Processar a imagem usando o serviço
    result = face_service.detect_face(image_data)

    return jsonify(result)
