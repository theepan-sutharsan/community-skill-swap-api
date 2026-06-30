from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.extensions import db
from app.models.swap_request_model import SwapRequest
from app.models.user_model import User


def create_swap_request(data):
    sender_id = int(get_jwt_identity())
    errors = _validate_swap_request_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    receiver_id = data["receiver_id"]

    if sender_id == receiver_id:
        return jsonify({"error": "You cannot send a request to yourself."}), 400

    receiver = User.query.get(receiver_id)
    if not receiver:
        return jsonify({"error": "Receiver not found."}), 404

    duplicate = SwapRequest.query.filter_by(
        sender_id=sender_id,
        receiver_id=receiver_id,
        status="pending",
    ).first()
    if duplicate:
        return jsonify({"error": "A pending request already exists."}), 400

    try:
        swap = SwapRequest(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=data.get("message", ""),
            status="pending",
        )
        db.session.add(swap)
        db.session.commit()
        return jsonify({
            "message": "Swap request sent.",
            "swap_request": swap.to_dict(),
        }), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Create failed."}), 500


def get_swap_requests():
    user_id = int(get_jwt_identity())
    query = SwapRequest.query

    if request.args.get("sent") == "1":
        query = query.filter_by(sender_id=user_id)
    elif request.args.get("received") == "1":
        query = query.filter_by(receiver_id=user_id)

    swaps = query.order_by(SwapRequest.created_at.desc()).all()
    return jsonify({"swap_requests": [s.to_dict() for s in swaps]}), 200


def get_swap_request(swap_id):
    swap = SwapRequest.query.get(swap_id)
    if not swap:
        return jsonify({"error": "Swap request not found."}), 404
    return jsonify({"swap_request": swap.to_dict()}), 200


def respond_swap_request(swap_id, data):
    user_id = int(get_jwt_identity())
    swap = SwapRequest.query.get(swap_id)

    if not swap:
        return jsonify({"error": "Swap request not found."}), 404
    if swap.receiver_id != user_id:
        return jsonify({"error": "Only the receiver can respond."}), 403
    if swap.status != "pending":
        return jsonify({"error": "This request is already handled."}), 400

    action = data.get("action")
    if action not in ["accepted", "declined"]:
        return jsonify({"errors": ["Action must be accepted or declined."]}), 400

    try:
        swap.status = action
        db.session.commit()
        return jsonify({
            "message": f"Request {action}.",
            "swap_request": swap.to_dict(),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Update failed."}), 500


def delete_swap_request(swap_id):
    user_id = int(get_jwt_identity())
    swap = SwapRequest.query.get(swap_id)

    if not swap:
        return jsonify({"error": "Swap request not found."}), 404
    if swap.sender_id != user_id:
        return jsonify({"error": "Only the sender can cancel."}), 403
    if swap.status != "pending":
        return jsonify({"error": "Only pending requests can be cancelled."}), 400

    try:
        db.session.delete(swap)
        db.session.commit()
        return jsonify({"message": "Swap request cancelled."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Delete failed."}), 500


def _validate_swap_request_payload(data):
    errors = []
    if not data.get("receiver_id"):
        errors.append("Receiver is required.")
    return errors
