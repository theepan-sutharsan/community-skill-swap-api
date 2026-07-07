import os

from flask_cors import CORS
from app import create_app
from app.extensions import db

from app.models import user_model, skill_model, user_skill_model
from app.models import swap_request_model, session_model

app = create_app()
CORS(app)


def init_db():
    with app.app_context():
        db.create_all()


try:
    init_db()
except Exception as exc:
    print(f"Database initialization skipped: {exc}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1", host="0.0.0.0", port=port)
