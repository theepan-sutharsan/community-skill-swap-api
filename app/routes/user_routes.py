from flask import Blueprint, request
from app.middleware import roles_required
from app.controllers import user_controller as ctrl

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/", methods=["GET"])
@roles_required("admin")
def list_users():
    return ctrl.get_users()


@users_bp.route("/<int:user_id>", methods=["GET"])
@roles_required("admin", "member")
def get_user(user_id):
    return ctrl.get_user(user_id)


@users_bp.route("/<int:user_id>", methods=["PUT"])
@roles_required("admin", "member")
def update_user(user_id):
    return ctrl.update_user(user_id, request.get_json() or {})


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@roles_required("admin")
def delete_user(user_id):
    return ctrl.delete_user(user_id)
