from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
