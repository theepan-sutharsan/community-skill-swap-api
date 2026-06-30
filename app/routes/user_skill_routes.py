from flask import Blueprint, request
from app.middleware import roles_required
from app.controllers import user_skill_controller as ctrl

user_skills_bp = Blueprint("user_skills", __name__, url_prefix="/api/user-skills")


@user_skills_bp.route("/", methods=["GET"])
@roles_required("member", "admin")
def list_user_skills():
    return ctrl.get_user_skills()


@user_skills_bp.route("/", methods=["POST"])
@roles_required("member")
def create_user_skill():
    return ctrl.create_user_skill(request.get_json() or {})


@user_skills_bp.route("/<int:entry_id>", methods=["GET"])
@roles_required("member", "admin")
def get_user_skill(entry_id):
    return ctrl.get_user_skill(entry_id)


@user_skills_bp.route("/<int:entry_id>", methods=["PUT"])
@roles_required("member")
def update_user_skill(entry_id):
    return ctrl.update_user_skill(entry_id, request.get_json() or {})


@user_skills_bp.route("/<int:entry_id>", methods=["DELETE"])
@roles_required("member")
def delete_user_skill(entry_id):
    return ctrl.delete_user_skill(entry_id)
