import re
from flask import jsonify, request
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user_model import User


def _validate_register_payload(data):
    errors = []
    if not data:
        return ["Request body is required."]

    email = data.get("email")
    if email is None or str(email).strip() == "":
        errors.append("email is required.")
    else:
        email_str = str(email).strip()
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email_str):
            errors.append("Invalid email format.")
        elif User.query.filter_by(email=email_str).first():
            errors.append("Email address already exists.")

    password = data.get("password")
    if password is None or str(password).strip() == "":
        errors.append("password is required.")
    elif len(str(password)) < 6:
        errors.append("password must be at least 6 characters long.")

    return errors


def _validate_login_payload(data):
    errors = []
    if not data:
        return ["Request body is required."]

    email = data.get("email")
    if email is None or str(email).strip() == "":
        errors.append("email is required.")

    password = data.get("password")
    if password is None or str(password).strip() == "":
        errors.append("password is required.")

    return errors


def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_register_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        user = User(
            email=str(data.get("email")).strip(),
            full_name=str(data.get("full_name")).strip() if data.get("full_name") else None,
            location=str(data.get("location")).strip() if data.get("location") else None,
            profile_image=str(data.get("profile_image")).strip() if data.get("profile_image") else None
        )
        user.set_password(str(data.get("password")))

        
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully.", "user": user.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_login_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        email_str = str(data.get("email")).strip()
        user = User.query.filter_by(email=email_str).first()

        if not user or not user.check_password(str(data.get("password"))):
            return jsonify({"error": "Invalid email or password."}), 401

        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "message": "Login successful.",
            "access_token": access_token,
            "user": user.to_dict()
        }), 200
    except Exception:
        return jsonify({"error": "An internal server error occurred."}), 500