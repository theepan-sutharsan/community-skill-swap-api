from flask import jsonify
from app.extensions import db
from app.models.user_model import User


def get_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({"users": [u.to_dict() for u in users]}), 200


def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    return jsonify({"user": user.to_dict()}), 200


def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    errors = _validate_user_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        if "name" in data:
            user.name = data["name"].strip()
        if "bio" in data:
            user.bio = data["bio"]
        if "location" in data:
            user.location = data["location"]
        if "avatar_url" in data:
            user.avatar_url = data["avatar_url"]
        if "role" in data and data["role"] in ["member", "admin"]:
            user.role = data["role"]

        db.session.commit()
        return jsonify({
            "message": "User updated.",
            "user": user.to_dict(),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Update failed."}), 500


def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Delete failed."}), 500


def _validate_user_payload(data):
    errors = []
    if "name" in data and not data["name"].strip():
        errors.append("Name cannot be empty.")
    if "role" in data and data["role"] not in ["member", "admin"]:
        errors.append("Role must be member or admin.")
    return errors
