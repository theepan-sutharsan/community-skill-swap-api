from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.utils import utc_now


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="member", nullable=False)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(150), nullable=True)
    avatar_url = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    user_skills = db.relationship("UserSkill", back_populates="user", lazy=True)
    sent_requests = db.relationship(
        "SwapRequest",
        foreign_keys="SwapRequest.sender_id",
        back_populates="sender",
        lazy=True,
    )
    received_requests = db.relationship(
        "SwapRequest",
        foreign_keys="SwapRequest.receiver_id",
        back_populates="receiver",
        lazy=True,
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "bio": self.bio,
            "location": self.location,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
