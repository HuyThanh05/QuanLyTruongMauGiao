# app/admin_views.py
from flask import redirect, request, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.security import generate_password_hash
from wtforms import PasswordField

from app import db
from app.models.Models import User, Role  # chỉnh đúng tên model bạn đang dùng


class SecureModelView(ModelView):
    """Chỉ Admin mới vào được Flask-Admin."""
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False

        # current_user.roles là list Role (bạn đang có ROLE_USER)
        roles = getattr(current_user, "roles", []) or []
        return any(getattr(r, "name", "") == "Admin" for r in roles)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login", next=request.url))  # auth = blueprint name của bạn


class UserAdminView(SecureModelView):
    # List view
    column_list = ("user_id", "name", "phone", "email", "status", "created_at", "lastLogin", "roles")
    column_labels = {
        "user_id": "ID",
        "name": "Họ tên",
        "phone": "SĐT",
        "email": "Email",
        "status": "Trạng thái",
        "created_at": "Ngày tạo",
        "lastLogin": "Đăng nhập gần nhất",
        "roles": "Vai trò",
    }

    # Ẩn password hash khỏi list + form
    column_exclude_list = ("password",)
    form_excluded_columns = ("password",)

    # Search / Filter
    column_searchable_list = ("name", "phone", "email")
    column_filters = ("status", "roles.name")

    # Thêm field nhập mật khẩu mới (không lưu plain)
    form_extra_fields = {
        "new_password": PasswordField("Mật khẩu mới")
    }

    def on_model_change(self, form, model, is_created):
        # Nếu nhập mật khẩu mới thì hash lại
        if form.new_password.data:
            # werkzeug sẽ ra dạng scrypt:... giống ảnh của bạn
            model.password = generate_password_hash(form.new_password.data, method="scrypt")


def init_flask_admin(app):
    # Mount Flask-Admin ở URL riêng để không đụng /admin hiện tại
    admin = Admin(
        app,
        name="Quản trị hệ thống",
        template_mode="bootstrap4",
        url="/admin-panel",
        endpoint="admin_panel",
    )

    admin.add_view(UserAdminView(User, db.session, name="Người dùng", endpoint="user"))
    admin.add_view(SecureModelView(Role, db.session, name="Vai trò", endpoint="role"))

    return admin
