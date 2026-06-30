from flask import Blueprint, request
from app.middleware import roles_required
from app.controllers import skill_controller as ctrl

skills_bp = Blueprint("skills", __name__, url_prefix="/api/skills")


@skills_bp.route("/", methods=["GET"])
def list_skills():
    return ctrl.get_skills()


@skills_bp.route("/", methods=["POST"])
@roles_required("admin")
def create_skill():
    return ctrl.create_skill(request.get_json() or {})


@skills_bp.route("/import-csv", methods=["POST"])
@roles_required("admin")
def import_skills_csv():
    return ctrl.import_skills_csv()


@skills_bp.route("/export/csv", methods=["GET"])
@roles_required("admin")
def export_skills_csv():
    return ctrl.export_skills_csv()


@skills_bp.route("/export/pdf", methods=["GET"])
@roles_required("admin")
def export_skills_pdf():
    return ctrl.export_skills_pdf()


@skills_bp.route("/<int:skill_id>", methods=["GET"])
def get_skill(skill_id):
    return ctrl.get_skill(skill_id)


@skills_bp.route("/<int:skill_id>", methods=["PUT"])
@roles_required("admin")
def update_skill(skill_id):
    return ctrl.update_skill(skill_id, request.get_json() or {})


@skills_bp.route("/<int:skill_id>", methods=["DELETE"])
@roles_required("admin")
def delete_skill(skill_id):
    return ctrl.delete_skill(skill_id)
