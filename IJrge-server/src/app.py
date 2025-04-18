from flask import Flask
from api.routes import register_routes


if __name__ == "__main__":
    app = Flask(__name__)

    register_routes(app)
    app.run(debug=True, host="0.0.0.0", port=5000)
