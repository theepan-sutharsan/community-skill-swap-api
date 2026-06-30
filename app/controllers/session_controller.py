from datetime import datetime, timezone
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.extensions import db
from app.models.session_model import Session
from app.models.swap_request_model import SwapRequest


def create_session(data):
    user_id = int(get_jwt_identity())
    errors = _validate_session_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    swap = SwapRequest.query.get(data["swap_request_id"])
    if not swap:
        return jsonify({"error": "Swap request not found."}), 404
    if swap.status != "accepted":
        return jsonify({"error": "Session can only be created for accepted swaps."}), 400
    if user_id not in [swap.sender_id, swap.receiver_id]:
        return jsonify({"error": "You are not part of this swap."}), 403

    existing = Session.query.filter_by(swap_request_id=swap.id).first()
    if existing:
        return jsonify({"error": "Session already exists for this swap."}), 400

    scheduled_at = datetime.fromisoformat(data["scheduled_at"].replace("Z", "+00:00"))
    if scheduled_at.tzinfo is None:
        scheduled_at = scheduled_at.replace(tzinfo=timezone.utc)

    if scheduled_at <= datetime.now(timezone.utc):
        return jsonify({"error": "Scheduled time must be in the future."}), 400

    try:
        session = Session(
            swap_request_id=data["swap_request_id"],
            scheduled_at=scheduled_at,
            location_or_link=data["location_or_link"].strip(),
            notes=data.get("notes", ""),
        )
        db.session.add(session)
        db.session.commit()
        return jsonify({
            "message": "Session scheduled.",
            "session": session.to_dict(),
        }), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Create failed."}), 500


def get_sessions():
    user_id = int(get_jwt_identity())

    swaps = SwapRequest.query.filter(
        (SwapRequest.sender_id == user_id) | (SwapRequest.receiver_id == user_id)
    ).all()
    swap_ids = [s.id for s in swaps]

    sessions = Session.query.filter(
        Session.swap_request_id.in_(swap_ids)
    ).order_by(Session.scheduled_at.desc()).all()

    return jsonify({"sessions": [s.to_dict() for s in sessions]}), 200


def get_session(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found."}), 404
    return jsonify({"session": session.to_dict()}), 200


def update_session(session_id, data):
    user_id = int(get_jwt_identity())
    session = Session.query.get(session_id)

    if not session:
        return jsonify({"error": "Session not found."}), 404

    swap = session.swap_request
    if user_id not in [swap.sender_id, swap.receiver_id]:
        return jsonify({"error": "You are not part of this session."}), 403

    try:
        if "scheduled_at" in data:
            scheduled_at = datetime.fromisoformat(
                data["scheduled_at"].replace("Z", "+00:00")
            )
            if scheduled_at.tzinfo is None:
                scheduled_at = scheduled_at.replace(tzinfo=timezone.utc)
            if scheduled_at <= datetime.now(timezone.utc):
                return jsonify({"error": "Scheduled time must be in the future."}), 400
            session.scheduled_at = scheduled_at

        if "location_or_link" in data:
            session.location_or_link = data["location_or_link"].strip()
        if "notes" in data:
            session.notes = data["notes"]

        db.session.commit()
        return jsonify({
            "message": "Session updated.",
            "session": session.to_dict(),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Update failed."}), 500


def delete_session(session_id):
    user_id = int(get_jwt_identity())
    session = Session.query.get(session_id)

    if not session:
        return jsonify({"error": "Session not found."}), 404

    swap = session.swap_request
    if user_id not in [swap.sender_id, swap.receiver_id]:
        return jsonify({"error": "You are not part of this session."}), 403

    try:
        db.session.delete(session)
        db.session.commit()
        return jsonify({"message": "Session cancelled."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Delete failed."}), 500


def _validate_session_payload(data):
    errors = []
    if not data.get("swap_request_id"):
        errors.append("Swap request is required.")
    if not data.get("scheduled_at"):
        errors.append("Scheduled date/time is required.")
    if not data.get("location_or_link") or not data["location_or_link"].strip():
        errors.append("Location or meeting link is required.")
    return errors
