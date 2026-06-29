from app.extensions import db
from app.utils import utc_now
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    profile_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=utc_now)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check the password against the stored hash."""
        return check_password_hash(self.password, password)

    def to_dict(self):
        """Return a dictionary representation of the user."""
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }