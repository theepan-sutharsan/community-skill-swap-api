from app.extensions import db
from app.utils import utc_now


class UserSkill(db.Model):
    __tablename__ = "user_skills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id"), nullable=False)
    type = db.Column(db.String(20), nullable=False) 
    level = db.Column(db.String(20), nullable=False) 
    created_at = db.Column(db.DateTime, default=utc_now)

    __table_args__ = (
        db.UniqueConstraint("user_id", "skill_id", "type", name="unique_user_skill_type"),
    )

    user = db.relationship("User", back_populates="user_skills")
    skill = db.relationship("Skill", back_populates="user_skills")

    def to_dict(self, include_user=False):
        skill_name = self.skill.name if self.skill else None
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "skill_id": self.skill_id,
            "skill_name": skill_name,
            "type": self.type,
            "level": self.level,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_user and self.user:
            data["user_name"] = self.user.name
            data["user_location"] = self.user.location
        return data
