from app.extensions import db
from app.utils import utc_now


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    swap_request_id = db.Column(
        db.Integer, db.ForeignKey("swap_requests.id"), unique=True, nullable=False
    )
    scheduled_at = db.Column(db.DateTime, nullable=False)
    location_or_link = db.Column(db.String(300), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    swap_request = db.relationship("SwapRequest", back_populates="session")

    def to_dict(self):
        return {
            "id": self.id,
            "swap_request_id": self.swap_request_id,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "location_or_link": self.location_or_link,
            "notes": self.notes,
            # "created_at": self.created_at.isoformat() if self.created_at else None,
        }
