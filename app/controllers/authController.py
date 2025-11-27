from flask import Blueprint, request, jsonify, url_for, redirect, flash, render_template, current_app
from flask_login import login_user, logout_user, current_user, login_required
from flask_principal import identity_changed, Identity
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.Models import User, Role
from app import db

authController = Blueprint('authController', __name__)

@authController.route('/signup', methods=['POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('routeController.home'))

    # get data from form
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    confirm_password = request.form.get('confirmPassword')
    teacher_role = Role.query.filter_by(name='teacher').first()

    if not teacher_role:
        print("Teacher role not found.")
        return redirect(url_for('routeController.signup'))
    
    # Data Validation
    if not email or not password or not phone:
        flash('Vui lòng nhập đầy đủ thông tin', 'error')
        return redirect(url_for('routeController.signup'))
    
    if password != confirm_password:
        flash('Mật khẩu xác nhận không khớp', 'error')
        return redirect(url_for('routeController.signup'))
    
    # Check if email already exists
    existing = User.query.filter_by(email=email).first()
    if existing:
        flash('Email đã được sử dụng', 'error')
        return redirect(url_for('routeController.signup'))
    
    user = User(email=email, phone=phone, password_hash=generate_password_hash(password))
    user.roles.append(teacher_role)
    db.session.add(user)
    db.session.commit()
    
    flash('Đăng ký thành công! Vui lòng đăng nhập', 'success')
    return redirect(url_for('routeController.signup'))

@authController.route('/login', methods=['POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('routeController.home'))

    # Get data from form
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Data Validation
    if not email or not password:
        flash('Vui lòng nhập đầy đủ thông tin', 'error')
        return redirect(url_for('routeController.signup'))
    
    # Check if email and password are correct
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        identity_changed.send(
            current_app,
            identity=Identity(user.id)
        )
        flash('Đăng nhập thành công!', 'success')
        return redirect(url_for('routeController.home'))
    
    flash('Email hoặc mật khẩu không đúng', 'error')
    return redirect(url_for('routeController.signup'))

@authController.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('routeController.home'))