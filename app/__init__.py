from flask import Flask
from flask_admin.theme import Bootstrap4Theme
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,current_user
from flask_migrate import Migrate
from flask_babel import Babel

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin(
    name="microblog",
    theme=Bootstrap4Theme(swatch="cerulean"),
)
babel = Babel()

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:password@localhost/educa?charset=utf8mb4",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY="khoideptrai",
    )

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "routeController.signup"
    login_manager.login_message = "Bạn phải đăng nhập để xem chức năng này"
    babel.init_app(app)
    
    # Import models
    from app.models.Models import User, Role, Student
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create tables if not exist
    with app.app_context():
        db.create_all()

    from app.controllers.routeController import routeController
    from app.controllers.authController import authController

    app.register_blueprint(routeController)
    app.register_blueprint(authController)

    # flask-admin
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Student, db.session))

    return app


