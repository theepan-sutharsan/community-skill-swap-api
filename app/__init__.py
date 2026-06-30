from datetime import timedelta
from flask import Flask, jsonify
from app.config import Config
from app.extensions import db, jwt
from app.routes import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        minutes=Config.JWT_ACCESS_TOKEN_EXPIRES_MINUTES
    )

    db.init_app(app)
    jwt.init_app(app)

    register_blueprints(app)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found."}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Server error."}), 500

    return app
