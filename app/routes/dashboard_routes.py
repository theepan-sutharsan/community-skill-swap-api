from flask import Blueprint
from app.middleware import roles_required
from app.controllers import dashboard_controller as ctrl

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_bp.route("/", methods=["GET"])
@roles_required("member", "admin")
def get_dashboard():
    return ctrl.get_dashboard()
