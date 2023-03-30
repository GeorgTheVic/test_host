import os
from flask_babelex import Babel
from flask import Flask, render_template, session, Response, redirect
from flask_admin import Admin
from flask_admin.contrib import sqla
from models import Info, db
from decouple import config
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException
from forms import ContactForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
babel = Babel(app)
csrf = CSRFProtect(app)
basic_auth = BasicAuth(app)

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(os.getcwd()) + "/site.db"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

app.config["SECRET_KEY"] = config("SECRET_KEY")


@babel.localeselector
def get_locale():
    return session.get("lang", "ru")


@app.route("/", methods=["GET", "POST"])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        pass
    info = Info.query.first_or_404()
    return render_template("app/index.html", info=info, form=form)


app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
app.config["BASIC_AUTH_USERNAME"] = config("INVESTOR_USERNAME")
app.config["BASIC_AUTH_PASSWORD"] = config("INVESTOR_PASSWORD")


class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException("Not authenticated.")
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(
            message,
            Response(
                "You could not be authenticated. Please refresh the page.",
                401,
                {"WWW-Authenticate": 'Basic realm="Login Required"'},
            ),
        )


admin = Admin(app, name="Инвестиции", template_mode="bootstrap4")
admin.add_view(ModelView(Info, db.session))

# only once
# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run()
