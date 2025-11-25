from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    password_hash = db.Column(db.String(255),nullable = False)
    
    # Flask-Login properties
    @property
    def is_active(self):
        return True
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return f"User({self.id}, {self.email}, {self.phone})"