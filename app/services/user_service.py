from werkzeug.security import generate_password_hash

from app import db
from app.models.Models import Role, User


class EmailAlreadyExists(Exception):
    """Raised khi email đã tồn tại trong hệ thống."""
    pass


def _get_or_create_role(role_name: str) -> Role:
    role = Role.query.filter_by(name=role_name).first()
    if role:
        return role

    # Tự động tạo role nếu chưa tồn tại để tránh lỗi khi tạo user mặc định
    role = Role(name=role_name)
    db.session.add(role)
    db.session.flush()  # đảm bảo role có id trước khi gán
    return role


def create_user_account(
    name: str,
    email: str,
    phone: str,
    password: str,
    role_name: str | None = None,
    allow_custom_role: bool = False,
) -> User:
    """
    Tạo tài khoản người dùng.
    - Mặc định chỉ gán role "Parent".
    - allow_custom_role=True mới cho chọn role_name khác.
    """
    if User.query.filter_by(email=email).first():
        raise EmailAlreadyExists()

    # Chặn người dùng tự chọn role; chỉ admin/service nội bộ mới bật allow_custom_role
    if allow_custom_role and role_name:
        role_to_use = role_name
    else:
        role_to_use = "Parent"

    role = _get_or_create_role(role_to_use)

    user = User(
        name=name or "guest",
        email=email,
        phone=phone,
        password_hash=generate_password_hash(password),
    )
    user.roles.append(role)

    db.session.add(user)
    db.session.commit()
    return user