from flask import Blueprint, request
from app.middleware import roles_required
from app.controllers import auth_controller as ctrl

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    return ctrl.register(request.get_json() or {})


@auth_bp.route("/login", methods=["POST"])
def login():
    return ctrl.login(request.get_json() or {})


@auth_bp.route("/me", methods=["GET"])
@roles_required("member", "admin")
def me():
    return ctrl.get_me()
