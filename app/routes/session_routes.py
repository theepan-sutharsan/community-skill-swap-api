from flask import Blueprint, request
from app.middleware import roles_required
from app.controllers import session_controller as ctrl

sessions_bp = Blueprint("sessions", __name__, url_prefix="/api/sessions")


@sessions_bp.route("/", methods=["GET"])
@roles_required("member", "admin")
def list_sessions():
    return ctrl.get_sessions()


@sessions_bp.route("/", methods=["POST"])
@roles_required("member")
def create_session():
    return ctrl.create_session(request.get_json() or {})


@sessions_bp.route("/<int:session_id>", methods=["GET"])
@roles_required("member", "admin")
def get_session(session_id):
    return ctrl.get_session(session_id)


@sessions_bp.route("/<int:session_id>", methods=["PUT"])
@roles_required("member")
def update_session(session_id):
    return ctrl.update_session(session_id, request.get_json() or {})


@sessions_bp.route("/<int:session_id>", methods=["DELETE"])
@roles_required("member")
def delete_session(session_id):
    return ctrl.delete_session(session_id)
