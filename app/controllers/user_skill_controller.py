from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.extensions import db
from app.models.user_skill_model import UserSkill
from app.models.skill_model import Skill


def create_user_skill(data):
    user_id = int(get_jwt_identity())
    errors = _validate_user_skill_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    skill = Skill.query.get(data["skill_id"])
    if not skill:
        return jsonify({"error": "Skill not found."}), 404

    existing = UserSkill.query.filter_by(
        user_id=user_id,
        skill_id=data["skill_id"],
        type=data["type"],
    ).first()
    if existing:
        return jsonify({"error": "You already posted this skill with this type."}), 400

    try:
        entry = UserSkill(
            user_id=user_id,
            skill_id=data["skill_id"],
            type=data["type"],
            level=data["level"],
        )
        db.session.add(entry)
        db.session.commit()
        return jsonify({
            "message": "Skill added to profile.",
            "user_skill": entry.to_dict(),
        }), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Create failed."}), 500


def get_user_skills():
    query = UserSkill.query

    skill_type = request.args.get("type", "").strip()
    user_id = request.args.get("user_id", "").strip()

    if skill_type:
        query = query.filter_by(type=skill_type)
    if user_id:
        query = query.filter_by(user_id=int(user_id))

    entries = query.order_by(UserSkill.created_at.desc()).all()
    return jsonify({"user_skills": [e.to_dict() for e in entries]}), 200


def get_user_skill(entry_id):
    entry = UserSkill.query.get(entry_id)
    if not entry:
        return jsonify({"error": "User skill not found."}), 404
    return jsonify({"user_skill": entry.to_dict()}), 200


def update_user_skill(entry_id, data):
    user_id = int(get_jwt_identity())
    entry = UserSkill.query.get(entry_id)

    if not entry:
        return jsonify({"error": "User skill not found."}), 404
    if entry.user_id != user_id:
        return jsonify({"error": "You can only edit your own skills."}), 403

    if "type" in data and data["type"] not in ["offered", "wanted"]:
        return jsonify({"errors": ["Type must be offered or wanted."]}), 400
    if "level" in data and data["level"] not in ["beginner", "intermediate", "expert"]:
        return jsonify({"errors": ["Level must be beginner, intermediate, or expert."]}), 400

    try:
        if "type" in data:
            entry.type = data["type"]
        if "level" in data:
            entry.level = data["level"]
        db.session.commit()
        return jsonify({
            "message": "User skill updated.",
            "user_skill": entry.to_dict(),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Update failed."}), 500


def delete_user_skill(entry_id):
    user_id = int(get_jwt_identity())
    entry = UserSkill.query.get(entry_id)

    if not entry:
        return jsonify({"error": "User skill not found."}), 404
    if entry.user_id != user_id:
        return jsonify({"error": "You can only delete your own skills."}), 403

    try:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message": "Skill removed from profile."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Delete failed."}), 500


def _validate_user_skill_payload(data):
    errors = []
    if not data.get("skill_id"):
        errors.append("Skill is required.")
    if data.get("type") not in ["offered", "wanted"]:
        errors.append("Type must be offered or wanted.")
    if data.get("level") not in ["beginner", "intermediate", "expert"]:
        errors.append("Level must be beginner, intermediate, or expert.")
    return errors
