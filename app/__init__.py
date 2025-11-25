from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///database.sqlite3",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY="dev-secret-key",
    )

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "authController.login"

    # Import models để đăng ký với SQLAlchemy
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Tạo bảng nếu chưa tồn tại
    with app.app_context():
        db.create_all()

    from app.controllers.routeController import routeController
    from app.controllers.authController import authController

    app.register_blueprint(routeController)
    app.register_blueprint(authController)

    return app