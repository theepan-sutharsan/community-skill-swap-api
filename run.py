from flask_cors import CORS
from app import create_app
from app.extensions import db

from app.models import user_model, skill_model, user_skill_model
from app.models import swap_request_model, session_model

app = create_app()
CORS(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
