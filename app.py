import os
from flask_babelex import Babel
from flask import Flask, render_template, session, Response, redirect
from flask_admin import Admin
from flask_admin.contrib import sqla
from models import Info, db
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException
from forms import ContactForm
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message
from config import Config

# from utils import get_text_message_input, send_message

app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)
csrf = CSRFProtect(app)
basic_auth = BasicAuth(app)
mail = Mail(app)

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(os.getcwd()) + "/site.db"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app)


@babel.localeselector
def get_locale():
    return session.get("lang", "ru")


@app.route("/", methods=["GET", "POST"])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(
            "Заявка от возможного инвестора",
            sender="noreply@demo.com",
            recipients=["somedayistheday1@gmail.com"],
        )
        msg.body = f"""
        Имя: {form.name.data}
        Номер телефона: {form.phone.data}
        Возраст: {form.age.data}
        Есть ли опыт инвестирования: {form.investing_exp.data}
        Почему именно фитнес: {form.why_fitness.data}
        Есть ли действующий бизнес: {form.has_business.data}
        Осведомлены ли, что минимально возможно покупка это 1% доли: {form.min_buying_share.data}"""

        mail.send(msg)
    info = Info.query.first_or_404()
    return render_template("app/index.html", info=info, form=form)


# @app.route("/send", methods=["POST"])
# async def send():
#     data = get_text_message_input(
#         app.config["RECIPIENT_WAID"],
#         "Yeah, yeah",
#     )
#     await send_message(data)
#     return redirect(url_for("index"))


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
