from flask import Flask, render_template

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

from app.controllers.routes import routes
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)