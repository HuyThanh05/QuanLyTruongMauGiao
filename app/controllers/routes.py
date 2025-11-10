from flask import Blueprint, render_template, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.users import User
from app import db

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('home.html',Title='Trang chủ')

@routes.route('/student')
def student():
    return render_template('student.html',Title='Danh sách học sinh')

@routes.route('/health')
def health():
    return render_template('health.html',Title='Sức khỏe')

@routes.route('/schedule')
def schedule():
    return render_template('schedule.html',Title='Lịch học')

@routes.route('/fee')
def fee():
    return render_template('fee.html',Title='Học phí')

@routes.route('/report')
def report():
    return render_template('report.html',Title='Báo cáo')

@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('login.html')
