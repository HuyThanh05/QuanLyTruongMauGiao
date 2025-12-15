from flask import Blueprint, render_template, redirect, url_for, abort, request, jsonify
from flask_login import login_required, current_user
from functools import wraps

from app.models.Models import Classroom, Student
from app.services.class_service import get_all_class
from app.services.health_record_service import count_student_record, count_students_recorded_today, count_students_not_recorded_today
from app.services.student_service import get_all_students, total_student, search_students, \
    get_student_count_by_classroom, total_male_count, total_female_count, classroom_student_count, get_gender_stats_by_class
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user

from app.models.Models import Classroom
from app.services.setting_service import get_or_create_settings, update_settings
from app.services.notification_service import create_notification, get_notifications_for_role
from app.services.classroom_service import get_teachers, assign_teacher_to_class


page_routes = Blueprint('pages', __name__)

#decorator wrap login_required for rbac
def roles_required(*role_names):
    """Custom decorator to check if user has required roles."""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            user_roles = [role.name for role in current_user.roles]
            if not any(role in user_roles for role in role_names):
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@page_routes.route('/')
def home():
    if current_user.is_authenticated:
        user_roles = [role.name for role in current_user.roles]
        if 'Admin' in user_roles:
            return redirect(url_for('admin.index'))
    return render_template('pages/home.html', Title='Trang chủ')


@page_routes.route('/student',methods=['POST','GET'])
@roles_required('Teacher')
def student():
    all_classrooms = get_all_class()
    total_students = total_student(all_classrooms)

    classroom_student_counts = {}
    for classroom in all_classrooms:
        classroom_student_counts[classroom.id] = get_student_count_by_classroom(classroom.id)

    q = request.args.get('q','',type = str).strip()
    
    students = search_students(q)

    return render_template('pages/student.html', Title='Danh sách học sinh', students=students, classrooms=all_classrooms, total_students=total_students, classroom_student_counts=classroom_student_counts)


@page_routes.route('/health')
@roles_required('Teacher')
def health():
    from app.models.Models import HealthRecord
    all_classrooms = Classroom.query.all()
    all_students = Student.query.all()
    recorded_students = count_students_recorded_today()
    unrecorded_students = count_students_not_recorded_today()

    return render_template('pages/health.html', Title='Sức khỏe',students=all_students,classrooms=all_classrooms,recorded_students=recorded_students,unrecorded_students=unrecorded_students)

@page_routes.route('/classsize')
@roles_required('Teacher')
def classsize():
    all_classrooms = Classroom.query.all()
    all_students = Student.query.all()
    capacity = 100
    total_students = total_student(all_classrooms)
    male_count = total_male_count()
    female_count = total_female_count()
    

    gender_stats_by_class = get_gender_stats_by_class(all_classrooms)
    
    return render_template('pages/classSize.html', Title="Quản lý sĩ số lớp", classrooms=all_classrooms, students=all_students, classroom_student_count=classroom_student_count(), male_count=male_count, female_count=female_count, total_students=total_students,capacity=capacity, get_gender_stats_by_class=gender_stats_by_class)

@page_routes.route('/fee')
@roles_required('Accountant')
def fee():
    return render_template('pages/fee.html', Title='Học phí')

@page_routes.route('/report')
@roles_required('Accountant')
def report():
    return render_template('pages/report.html', Title='Doanh thu')

@page_routes.route('/studentprofile')
@roles_required('Parent')
def studentprofile():
    return render_template('pages/studentProfile.html', Title = "Quản lý hồ sơ")

@page_routes.route('/kidtracking')
@roles_required('Parent')
def kid():
    parent_id = current_user.id
    student = Student.query.filter_by(parent_id=parent_id).first()
    count = count_student_record(student.id)
    return render_template('pages/kid.html',Title = "Thông tin trẻ",parent_id=parent_id,student_id=student.id if student else None,count=count)

@page_routes.route('/feetracking')
@roles_required('Parent')
def feetracking():
    return render_template('pages/feeTracking.html', Title = "Theo dõi học phí")


@page_routes.route('/signup', methods=['GET'])
def signup():
    if current_user.is_authenticated:
        user_roles = [role.name for role in current_user.roles]
        if 'Admin' in user_roles:
            return redirect(url_for('admin.index'))
    return render_template('pages/login.html')

@page_routes.route('/administrator')
@roles_required('Admin')
def administrator():
    return redirect(url_for('admin.index'))


@page_routes.route("/admin/dashboard")
@roles_required("Admin")
def admin_dashboard():
    return render_template("pages/admin/dashboard.html")

@page_routes.route("/admin/settings", methods=["GET", "POST"])
@roles_required("Admin")
def admin_settings():
    if request.method == "GET":
        s = get_or_create_settings()
        return render_template("pages/admin/settings.html", s=s)

    tuition_base = request.form.get("tuition_base", 0)
    meal_fee_per_day = request.form.get("meal_fee_per_day", 0)
    max_students_per_class = request.form.get("max_students_per_class", 30)

    s = update_settings(tuition_base, meal_fee_per_day, max_students_per_class, updated_by=current_user.id)

    # Tự tạo thông báo sau khi đổi quy định
    title = "Cập nhật quy định thu phí"
    content = (f"Học phí cơ bản: {s.tuition_base} | "
               f"Tiền ăn/ngày: {s.meal_fee_per_day} | "
               f"Sĩ số tối đa/lớp: {s.max_students_per_class}.")
    create_notification(title, content, target_role="All", created_by=current_user.id)

    flash("Đã cập nhật quy định và tạo thông báo.", "success")
    return redirect(url_for("page_routes.admin_settings"))

@page_routes.route("/admin/teaching-assign", methods=["GET", "POST"])
@roles_required("Admin")
def admin_teaching_assign():
    if request.method == "GET":
        classrooms = Classroom.query.all()
        teachers = get_teachers()
        return render_template("pages/admin/teaching_assign.html", classrooms=classrooms, teachers=teachers)

    class_id = request.form.get("class_id", type=int)
    teacher_id = request.form.get("teacher_id", type=int)  # để trống -> None

    classroom, err = assign_teacher_to_class(class_id, teacher_id)
    if err:
        flash(err, "danger")
        return redirect(url_for("page_routes.admin_teaching_assign"))

    flash("Đã lưu phân công giảng dạy.", "success")
    return redirect(url_for("page_routes.admin_teaching_assign"))

@page_routes.route("/admin/notifications", methods=["GET", "POST"])
@roles_required("Admin")
def admin_notifications():
    if request.method == "GET":
        return render_template("pages/admin/notifications.html")

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    target_role = request.form.get("target_role", "All")

    if not title or not content:
        flash("Thiếu tiêu đề hoặc nội dung.", "danger")
        return redirect(url_for("page_routes.admin_notifications"))

    create_notification(title, content, target_role=target_role, created_by=current_user.id)
    flash("Đã gửi thông báo.", "success")
    return redirect(url_for("page_routes.admin_notifications"))


@page_routes.route("/parent/notifications")
@roles_required("Parent")
def parent_notifications():
    notis = get_notifications_for_role("Parent")
    return render_template("pages/parentNotification.html", notis=notis)


@page_routes.route("/admin/reports")
@roles_required("Admin")
def admin_reports():
    return render_template("pages/report.html", Title="Doanh thu")
