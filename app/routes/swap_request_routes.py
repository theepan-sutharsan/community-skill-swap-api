from flask import Blueprint, request
from app.middleware import roles_required
from app.controllers import swap_request_controller as ctrl

swap_requests_bp = Blueprint("swap_requests", __name__, url_prefix="/api/swap-requests")


@swap_requests_bp.route("/", methods=["GET"])
@roles_required("member", "admin")
def list_swap_requests():
    return ctrl.get_swap_requests()


@swap_requests_bp.route("/", methods=["POST"])
@roles_required("member")
def create_swap_request():
    return ctrl.create_swap_request(request.get_json() or {})


@swap_requests_bp.route("/<int:swap_id>", methods=["GET"])
@roles_required("member", "admin")
def get_swap_request(swap_id):
    return ctrl.get_swap_request(swap_id)


@swap_requests_bp.route("/<int:swap_id>/respond", methods=["PUT"])
@roles_required("member")
def respond_swap_request(swap_id):
    return ctrl.respond_swap_request(swap_id, request.get_json() or {})


@swap_requests_bp.route("/<int:swap_id>", methods=["DELETE"])
@roles_required("member")
def delete_swap_request(swap_id):
    return ctrl.delete_swap_request(swap_id)
