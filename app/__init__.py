from flask import Flask, redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_admin.menu import MenuLink
from flask_login import current_user
from flask_migrate import Migrate
from flask import flash

from app.extensions import db, login_manager, admin, babel


class SecureModelView(ModelView):
    # Ẩn trên danh sách
    column_exclude_list = ("password_hash", "account_status")
    # Ẩn trong form Create/Edit
    form_excluded_columns = ("password_hash", "account_status")
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        roles = getattr(current_user, "roles", []) or []
        return any(getattr(r, "name", "") == "Admin" for r in roles)

    def inaccessible_callback(self, name, **kwargs):
        # /login của bạn chỉ POST => redirect về trang có form login/signup
        return redirect(url_for("pages.signup", next=request.url))

class UserAdminView(SecureModelView):
    # ✅ Bảng list chỉ hiện các cột cần thiết
    column_list = ("name", "phone", "email", "roles", "last_login", "created_at")

    # ✅ Ẩn cột nhạy cảm khỏi list
    column_exclude_list = ("password_hash", "account_status")

    # ✅ Form Create/Edit chỉ cho sửa các field này
    form_columns = ("name", "phone", "email", "roles")

    # ✅ Ẩn các field không nên chỉnh bằng tay
    form_excluded_columns = (
        "password_hash",
        "account_status",
        "children",
        "health_records_made",
        "last_login",
        "created_at",
    )

    # ✅ Đổi tên hiển thị cho đẹp
    column_labels = {
        "name": "Họ tên",
        "phone": "SĐT",
        "email": "Email",
        "roles": "Vai trò",
        "last_login": "Đăng nhập gần nhất",
        "created_at": "Ngày tạo",
    }


class QuyDinhView(BaseView):
    def is_accessible(self):
        return SecureModelView.is_accessible(self)

    def inaccessible_callback(self, name, **kwargs):
        return SecureModelView.inaccessible_callback(self, name, **kwargs)

    @expose("/")
    def index(self):
        return self.render("admin/quydinh.html")


class ThongBaoView(BaseView):
    def is_accessible(self):
        return SecureModelView.is_accessible(self)

    def inaccessible_callback(self, name, **kwargs):
        return SecureModelView.inaccessible_callback(self, name, **kwargs)

    @expose("/", methods=("GET", "POST"))   # ✅ cho phép POST
    def index(self):
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            content = request.form.get("content", "").strip()
            target = request.form.get("target", "all")

            flash(f"Đã tạo thông báo: '{title}' | Gửi tới: {target}", "success")

        return self.render("admin/thongbao.html")


class BaoCaoView(BaseView):
    def is_accessible(self):
        return SecureModelView.is_accessible(self)

    def inaccessible_callback(self, name, **kwargs):
        return SecureModelView.inaccessible_callback(self, name, **kwargs)

    @expose("/")
    def index(self):
        return self.render("admin/baocao.html")


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:hhthah05%HT@localhost/educa?charset=utf8mb4",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY="khoideptrai",
    )

    # init extensions
    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "pages.signup"
    login_manager.login_message = "Bạn phải đăng nhập để xem chức năng này"

    babel.init_app(app)

    # Import models (sau khi db đã init)
    from app.models.Models import User, Role, Student  # noqa: F401

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create tables if not exist
    with app.app_context():
        db.create_all()

    # Register blueprints
    from app.controllers.page_routes import page_routes
    from app.controllers.auth_routes import auth_service
    from app.controllers.user_api import user_api
    from app.controllers.student_api import student_api
    from app.controllers.kid_api import kid_api
    from app.controllers.health_api import health_api
    from app.controllers.tuitionFee_api import tuitionFee_api

    app.register_blueprint(page_routes)
    app.register_blueprint(auth_service)
    app.register_blueprint(user_api, url_prefix="/api/users")
    app.register_blueprint(student_api)
    app.register_blueprint(kid_api)
    app.register_blueprint(health_api)
    app.register_blueprint(tuitionFee_api)

    # Flask-Admin
    admin.init_app(app)

    admin.add_view(UserAdminView(User, db.session, name="Quản lý người dùng"))
    admin.add_view(QuyDinhView(name="Thay đổi quy định", endpoint="quy-dinh"))
    admin.add_view(ThongBaoView(name="Thông báo", endpoint="thong-bao"))
    admin.add_view(BaoCaoView(name="Xem báo cáo", endpoint="bao-cao"))

    # logout endpoint: auth.logout (Blueprint('auth', __name__))
    admin.add_link(MenuLink(name="Đăng xuất", url="/logout"))

    return app
