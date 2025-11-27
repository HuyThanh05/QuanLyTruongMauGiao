from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from functools import wraps

from app import db
from app.models.Models import Role, roles_users, User

routeController = Blueprint('routeController', __name__)


def roles_required(*role_names):
    """Custom decorator to check if user has required roles."""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            
            # Check if user has any of the required roles
            user_roles = [role.name for role in current_user.roles]
            if not any(role in user_roles for role in role_names):
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@routeController.route('/')
def home():
    return render_template('pages/home.html', Title='Trang chủ')

@routeController.route('/student')
@roles_required('Teacher', 'Admin')
def student():
    return render_template('pages/student.html', Title='Danh sách học sinh')

@routeController.route('/health')
@roles_required('Teacher')
def health():
    return render_template('pages/health.html', Title='Sức khỏe')

@routeController.route('/schedule')
@roles_required('Teacher')
def schedule():
    return render_template('pages/schedule.html', Title='Lịch học')

@routeController.route('/fee')
@roles_required('Teacher')
def fee():
    return render_template('pages/fee.html', Title='Học phí')

@routeController.route('/report')
@roles_required('Teacher')
def report():
    return render_template('pages/report.html', Title='Báo cáo')

@routeController.route('/signup', methods=['GET'])
def signup():
    return render_template('pages/login.html')

@routeController.route('/administrator')
@roles_required('Admin')
def administrator():
    return redirect(url_for('admin.index'))