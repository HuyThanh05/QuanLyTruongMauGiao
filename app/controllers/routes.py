from flask import Blueprint, render_template
routes = Blueprint('routes', __name__)

@routes.route('/dashboard')
def dashboard():
    return render_template('home.html')

@routes.route('/signup')
def signup():
    return render_template('login.html')

# Route mặc định: chuyển về dashboard
@routes.route('/')
def index():
    return render_template('home.html')