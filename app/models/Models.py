from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime
from flask_login import UserMixin
from flask_security import RoleMixin

# roles_users = db.Table('roles_users',
#     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
# )

#Database Models
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10), nullable = False,unique=True)
    email = db.Column(db.String(50), nullable = False, unique = True)
    password_hash = db.Column(db.String(255),nullable = False)
    #relationships
    # roles = db.relationship('Role',secondary= roles_users,backref= 'roled')

    def __repr__(self):
        return f"User({self.id}, {self.email}, {self.phone})"

# class Role(db.Model, RoleMixin):
#     __tablename__ = "role"
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True, nullable=False)

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    parent_contact = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Student({self.id}, {self.name}, {self.age}, {self.class_name})"
