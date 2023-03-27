import os
from flask_babelex import Babel
from flask import Flask, render_template, request, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Info, db

app = Flask(__name__)
babel = Babel(app)

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.getcwd() + "site.db"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app)


# @babel.localeselector
# def get_locale():
#     if request.args.get("lang"):
#         session["lang"] = request.args.get("lang")
#     return session.get("lang", "en")


# only once
with app.app_context():
    db.create_all()

app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

admin = Admin(app, name="gym_investor", template_mode="bootstrap3")
admin.add_view(ModelView(Info, db.session))


@app.route("/")
def index():
    return render_template("app/index.html")


if __name__ == "__main__":
    app.run()
