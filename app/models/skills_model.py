from app.extensions import db
from app.utils import utc_now


class Skill(db.Model):
    __tablename__ = "skills"

    Skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Skill_name = db.Column(db.String(100), nullable=False)
    catogory = db.Column(db.String(120), nullable=False)
   


    def to_dict(self):
        return {
            "skill_id": self.Skill_id,
            "skill_name": self.Skill_name,
            "catogory":self.catogory,
        }
