from flask import Flask, Blueprint
from .health import health_bp
from .upload_image import upload_image_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")

# Registrar blueprints
api_bp.register_blueprint(health_bp)
api_bp.register_blueprint(upload_image_bp)

def register_routes(app: Flask):
    app.register_blueprint(api_bp)
