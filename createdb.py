from backend import backend
from data.provider import db

with backend.app_context():
    db.init_app(backend)
    db.create_all()