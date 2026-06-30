from flask import jsonify, request, Response
import csv
import io
from fpdf import FPDF
from app.extensions import db
from app.models.skill_model import Skill


def create_skill(data):
    errors = _validate_skill_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    existing = Skill.query.filter_by(name=data["name"].strip()).first()
    if existing:
        return jsonify({"error": "Skill name already exists."}), 400

    try:
        skill = Skill(
            name=data["name"].strip(),
            category=data["category"].strip(),
        )
        db.session.add(skill)
        db.session.commit()
        return jsonify({
            "message": "Skill created.",
            "skill": skill.to_dict(),
        }), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Create failed."}), 500


def get_skills():
    query = Skill.query

    search = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    if search:
        query = query.filter(Skill.name.ilike(f"%{search}%"))
    if category:
        query = query.filter(Skill.category.ilike(f"%{category}%"))

    skills = query.order_by(Skill.name).all()
    return jsonify({"skills": [s.to_dict() for s in skills]}), 200


def get_skill(skill_id):
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": "Skill not found."}), 404
    return jsonify({"skill": skill.to_dict()}), 200


def update_skill(skill_id, data):
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": "Skill not found."}), 404

    errors = _validate_skill_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    if data["name"].strip() != skill.name:
        existing = Skill.query.filter_by(name=data["name"].strip()).first()
        if existing:
            return jsonify({"error": "Skill name already exists."}), 400

    try:
        skill.name = data["name"].strip()
        skill.category = data["category"].strip()
        db.session.commit()
        return jsonify({
            "message": "Skill updated.",
            "skill": skill.to_dict(),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Update failed."}), 500


def delete_skill(skill_id):
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": "Skill not found."}), 404

    try:
        db.session.delete(skill)
        db.session.commit()
        return jsonify({"message": "Skill deleted."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Delete failed."}), 500


def _validate_skill_payload(data):
    errors = []
    if not data.get("name") or not data["name"].strip():
        errors.append("Skill name is required.")
    if not data.get("category") or not data["category"].strip():
        errors.append("Category is required.")
    return errors


def import_skills_csv():
    if "file" not in request.files:
        return jsonify({"error": "CSV file is required."}), 400

    file = request.files["file"]
    if not file.filename or not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Please upload a .csv file."}), 400

    try:
        content = file.read().decode("utf-8")
        reader = csv.reader(io.StringIO(content))

        imported = 0
        skipped = 0
        errors = []

        for row_num, row in enumerate(reader, start=1):
            if not row or all(not cell.strip() for cell in row):
                continue

            if row_num == 1 and row[0].strip().lower() == "name":
                continue

            if len(row) < 2:
                errors.append(f"Row {row_num}: need name and category.")
                continue

            name = row[0].strip()
            category = row[1].strip()

            if not name or not category:
                errors.append(f"Row {row_num}: name and category cannot be empty.")
                continue

            existing = Skill.query.filter_by(name=name).first()
            if existing:
                skipped += 1
                continue

            db.session.add(Skill(name=name, category=category))
            imported += 1

        db.session.commit()

        return jsonify({
            "message": "CSV import finished.",
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
        }), 200

    except Exception:
        db.session.rollback()
        return jsonify({"error": "CSV import failed."}), 500


def export_skills_csv():
    skills = Skill.query.order_by(Skill.category, Skill.name).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["name", "category"])

    for skill in skills:
        writer.writerow([skill.name, skill.category])

    csv_text = output.getvalue()
    return Response(
        csv_text,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=skills.csv"},
    )


def export_skills_pdf():
    skills = Skill.query.order_by(Skill.category, Skill.name).all()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "SkillSwap - Skills List", ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(80, 8, "Skill Name", border=1)
    pdf.cell(80, 8, "Category", border=1, ln=True)

    pdf.set_font("Helvetica", "", 11)
    for skill in skills:
        pdf.cell(80, 8, skill.name, border=1)
        pdf.cell(80, 8, skill.category, border=1, ln=True)

    pdf_bytes = pdf.output()

    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment; filename=skills.pdf"},
    )

