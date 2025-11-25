from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10), nullable = False,unique=True)
    email = db.Column(db.String(50), nullable = False, unique = True)
    password_hash = db.Column(db.String(255),nullable = False)

    def __repr__(self):
        return f"User({self.id}, {self.email}, {self.phone})"