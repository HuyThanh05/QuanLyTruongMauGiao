from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from functools import wraps

from app.models.Models import Classroom, Student

routeController = Blueprint('routeController', __name__)

#decorator wrap login_required for rbac
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
@roles_required('Teacher')
def student():
    all_classrooms = Classroom.query.all()
    all_students = Student.query.all()

    total_students = 0
    for classroom in all_classrooms:
         total_students += classroom.max_slots

    return render_template('pages/student.html', Title='Danh sách học sinh', students=all_students, classrooms=all_classrooms,total_students=total_students)

@routeController.route('/health')
@roles_required('Teacher')
def health():
    from app.models.Models import HealthRecord
    all_classrooms = Classroom.query.all()
    all_students = Student.query.all()

    return render_template('pages/health.html', Title='Sức khỏe',students=all_students,classrooms=all_classrooms)

@routeController.route('/schedule')
@roles_required('Teacher')
def schedule():
    return render_template('pages/schedule.html', Title='Lịch học')

@routeController.route('/fee')
@roles_required('Accountant')
def fee():
    return render_template('pages/fee.html', Title='Học phí')

@routeController.route('/report')
@roles_required('Accountant')
def report():
    return render_template('pages/report.html', Title='Doanh thu')

@routeController.route('/classsize')
@roles_required('Teacher')
def classsize():
    all_classrooms = Classroom.query.all()
    all_students = Student.query.all()

    classroom_student_count = {}
    for student in all_students:
        if student.class_id:
            if student.class_id in classroom_student_count:
                classroom_student_count[student.class_id] += 1
            else:
                classroom_student_count[student.class_id] = 1

    return render_template('pages/classSize.html', Title = "Quản lý sĩ số lớp", classrooms=all_classrooms, students=all_students, classroom_student_count=classroom_student_count)


@routeController.route('/studentprofile')
@roles_required('Parent')
def studentprofile():
    return render_template('pages/studentProfile.html', Title = "Quản lý hồ sơ")

@routeController.route('/kidtracking')
@roles_required('Parent')
def kid():
    return render_template('pages/kid.html',Title = "Thông tin trẻ")

@routeController.route('/feetracking')
@roles_required('Parent')
def feetracking():
    return render_template('pages/feeTracking.html', Title = "Theo dõi học phí")

@routeController.route('/parent/notification')
@roles_required('Parent')
def parentnotification():
    return render_template('pages/parentNotification.html', Title = "Thông báo")

@routeController.route('/signup', methods=['GET'])
def signup():
    return render_template('pages/login.html')

@routeController.route('/administrator')
@roles_required('Admin')
def administrator():
    return redirect(url_for('admin.index'))