from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    phone = StringField("Номер телефона", validators=[DataRequired()])
    age = IntegerField("Возраст", validators=[DataRequired()])
    investing_exp = StringField(
        "Есть ли опыт инвестирования?", validators=[DataRequired()]
    )
    why_fitness = StringField("Почему именно фитнес?", validators=[DataRequired()])
    has_business = StringField(
        "Есть ли действующий бизнес?", validators=[DataRequired()]
    )
    min_buying_share = StringField(
        "Осведомлены ли, что минимально возможно покупка это 1% доли?",
        validators=[DataRequired()],
    )
    submit = SubmitField("Отправить")
