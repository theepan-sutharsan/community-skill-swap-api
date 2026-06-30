from app import create_app
from app.extensions import db
from app.models.user_model import User
from app.models.skill_model import Skill


def seed():
    app = create_app()

    with app.app_context():
        db.create_all()

        sample_skills = [
            ("Python", "Tech"),
            ("Guitar", "Music"),
            ("Yoga", "Fitness"),
            ("Photography", "Art"),
            ("JavaScript", "Tech"),
            ("Spanish", "Language"),
        ]

        for name, category in sample_skills:
            exists = Skill.query.filter_by(name=name).first()
            if not exists:
                db.session.add(Skill(name=name, category=category))

        admin_email = "admin@skillswap.com"
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(
                name="Admin",
                email=admin_email,
                role="admin",
            )
            admin.set_password("admin123")
            db.session.add(admin)

        db.session.commit()
        print("Done! Skills and admin user added.")
        print("Admin login: admin@skillswap.com / admin123")


if __name__ == "__main__":
    seed()
