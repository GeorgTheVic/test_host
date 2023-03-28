import os
from flask_babelex import Babel
from flask import Flask, render_template, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Info, db
from decouple import config

app = Flask(__name__)
babel = Babel(app)

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(os.getcwd()) + "/site.db"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

app.config["SECRET_KEY"] = config("SECRET_KEY")


@babel.localeselector
def get_locale():
    return session.get("lang", "ru")


@app.route("/")
def index():
    info = Info.query.first_or_404()
    return render_template("app/index.html", info=info)


app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

admin = Admin(app, name="Инвестиции", template_mode="bootstrap4")
admin.add_view(ModelView(Info, db.session))

# only once
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
