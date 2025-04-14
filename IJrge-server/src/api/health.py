from flask import Blueprint, jsonify, request

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    Endpoint de healthcheck para verificar se a API está funcionando.
    """
    return jsonify({"status": "healthy", "message": "API is running"})
