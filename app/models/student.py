from sqlalchemy import Column, Integer, String
from app import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    class_name = db.Columnq(db.String(50), nullable=False)
    parent_contact = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Student({self.id}, {self.name}, {self.age}, {self.class_name})"
