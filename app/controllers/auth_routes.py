# Blueprint cho module xác thực
from flask import Blueprint, request, url_for, redirect, flash, current_app, session
from flask_login import login_user, logout_user, current_user
from flask_principal import identity_changed, Identity
from app.services.auth_service import (
    authenticate_user,
    signup_parent_user,
    MissingFieldError,
    PasswordMismatchError,
    InvalidCredentials,
    InvalidPhoneError,
)
from app.services.user_service import EmailAlreadyExists

# Khởi tạo Blueprint cho auth
auth_service = Blueprint("auth", __name__)

#  Điều hướng user
def redirect_by_role(user):
    roles = [r.name for r in user.roles]
    if "Admin" in roles:
        return redirect(url_for("admin.index"))
    return redirect(url_for("pages.home"))


# ĐĂNG KÝ
@auth_service.route("/signup", methods=["POST"])
def signup():
    if current_user.is_authenticated:
        return redirect_by_role(current_user)

    name = request.form.get("username")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmPassword")

    try:
        # Gọi service để tạo tài khoản mới
        signup_parent_user(
            name=name,
            email=email,
            phone=phone,
            password=password,
            confirm_password=confirm_password,
        )
        flash("Đăng ký thành công! Vui lòng đăng nhập", "success")
        return redirect(url_for("pages.signup", mode="login"))

    except MissingFieldError:
        flash("Vui lòng nhập đầy đủ thông tin", "register_error")
    except PasswordMismatchError:
        flash("Mật khẩu xác nhận không khớp", "register_error")
    except InvalidPhoneError:
        flash("Số điện thoại không hợp lệ", "register_error")
    except EmailAlreadyExists:
        flash("Email đã được sử dụng", "register_error")
    return redirect(url_for("pages.signup", mode="register"))


#  ĐĂNG NHẬP
@auth_service.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect_by_role(current_user)
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = authenticate_user(email, password)
        login_user(user)
        identity_changed.send(current_app, identity=Identity(user.id))
        flash("Đăng nhập thành công!", "success")
        return redirect_by_role(user)

    except MissingFieldError:
        flash("Vui lòng nhập đầy đủ thông tin", "error")
    except InvalidCredentials:
        flash("Email hoặc mật khẩu không đúng", "error")
    return redirect(url_for("pages.signup", mode="login"))


# ĐĂNG XUẤT
@auth_service.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    session.pop("_flashes", None)
    return redirect(url_for("pages.home"))
