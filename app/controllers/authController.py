from flask import Blueprint, request, jsonify, url_for, redirect
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.user import User
from app import db

authController = Blueprint('authController', __name__)

@authController.route('/signup', methods=['POST'])
def signup():
    
    mode = request.args.get('mode')
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Thiếu dữ liệu'}), 400

    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if not mode or mode != "register":
        return jsonify({'error': 'Mode phải là register'}), 400
    
    if not email or not password:
        return jsonify({'error': 'Thiếu email hoặc mật khẩu'}), 400
    
    if not phone:
        return jsonify({'error': 'Thiếu số điện thoại'}), 400
    
    # Xử lí logic đăng ký
    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({'error': 'Email đã được sử dụng'}), 400
    
    user = User(email=email, phone=phone, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Đăng ký thành công'}), 201

@authController.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    mode = request.args.get('mode')

    if not mode or mode != "login":
        return jsonify({'error': 'Mode phải là login'}), 400
    
    if not data:
        return jsonify({'error': 'Thiếu dữ liệu'}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Thiếu email hoặc mật khẩu'}), 400
    
    # Xử lí logic đăng nhập
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({'message': 'Đăng nhập thành công', 'redirect': url_for('routeController.home')}), 200
    
    return jsonify({'error': 'Email hoặc mật khẩu không đúng'}), 401

@authController.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('routeController.home'))