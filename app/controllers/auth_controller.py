from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta
from app.extensions import db
from app.models.user_model import User
from app.config import Config


def register(data):
    errors = _validate_register(data)
    if errors:
        return jsonify({"errors": errors}), 400

    existing = User.query.filter_by(email=data["email"].strip().lower()).first()
    if existing:
        return jsonify({"error": "Email already registered."}), 400

    try:
        user = User(
            name=data["name"].strip(),
            email=data["email"].strip().lower(),
            location=data.get("location", "").strip() or None,
            role="member",
        )
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "Registration successful.",
            "user": user.to_dict(),
        }), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Registration failed."}), 500


def login(data):
    if not data.get("email") or not data.get("password"):
        return jsonify({"errors": ["Email and password are required."]}), 400

    user = User.query.filter_by(email=data["email"].strip().lower()).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password."}), 401

    expires = timedelta(minutes=Config.JWT_ACCESS_TOKEN_EXPIRES_MINUTES)
    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role},
        expires_delta=expires,
    )

    return jsonify({
        "access_token": token,
        "user": user.to_dict(),
    }), 200


def get_me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found."}), 404

    return jsonify({"user": user.to_dict()}), 200


def _validate_register(data):
    errors = []

    if not data.get("name") or not data["name"].strip():
        errors.append("Name is required.")

    if not data.get("email") or not data["email"].strip():
        errors.append("Email is required.")

    if not data.get("password") or len(data["password"]) < 6:
        errors.append("Password must be at least 6 characters.")

    return errors
