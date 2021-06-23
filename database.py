import json
import time
from flask_sqlalchemy import SQLAlchemy

from app import app
db = SQLAlchemy(app)


class Users(db.Model):
    email = db.Column(db.String(20), nullable=True, unique=True, primary_key=True)
    access_token = db.Column(db.String(31), nullable=False, unique=True)
    refresh_token = db.Column(db.String(31), unique=True, nullable=False)
    scope = db.Column(db.String(30), nullable=False)
    exp = db.Column(db.Integer, nullable=False)

    def __init__(self, tokens, data):
        self.email = data["email"]
        self.exp = int(time.time()) + 50000
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]
        self.scope = tokens["scope"]

    def __repr__(self):
        k = json.dumps({"access_token": self.access_token, "refresh_token": self.refresh_token, "exp": self.exp})
        print(k)
        return k


db.create_all()
db.session.commit()
