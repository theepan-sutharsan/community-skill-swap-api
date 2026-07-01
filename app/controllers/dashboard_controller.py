from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user_skill_model import UserSkill
from app.models.swap_request_model import SwapRequest
from app.models.session_model import Session


def get_dashboard():
    user_id = int(get_jwt_identity())

    offered = UserSkill.query.filter_by(user_id=user_id, type="offered").all()
    wanted = UserSkill.query.filter_by(user_id=user_id, type="wanted").all()

    community_offered = (
        UserSkill.query.filter(
            UserSkill.user_id != user_id,
            UserSkill.type == "offered",
        )
        .order_by(UserSkill.created_at.desc())
        .all()
    )

    sent = SwapRequest.query.filter_by(sender_id=user_id).order_by(
        SwapRequest.created_at.desc()
    ).limit(5).all()

    received = SwapRequest.query.filter_by(receiver_id=user_id).order_by(
        SwapRequest.created_at.desc()
    ).limit(5).all()

    swaps = SwapRequest.query.filter(
        (SwapRequest.sender_id == user_id) | (SwapRequest.receiver_id == user_id),
        SwapRequest.status == "accepted",
    ).all()
    swap_ids = [s.id for s in swaps]

    sessions = Session.query.filter(
        Session.swap_request_id.in_(swap_ids)
    ).order_by(Session.scheduled_at.desc()).all()

    return jsonify({
        "my_skills_offered": [s.to_dict() for s in offered],
        "my_skills_wanted": [s.to_dict() for s in wanted],
        "community_skills_offered": [
            s.to_dict(include_user=True) for s in community_offered
        ],
        "requests_sent": [s.to_dict() for s in sent],
        "requests_received": [s.to_dict() for s in received],
        "confirmed_sessions": [s.to_dict() for s in sessions],
    }), 200
