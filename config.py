from decouple import config


class Config:
    SECRET_KEY = config("SECRET_KEY")
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config("MAIL_USERNAME")
    MAIL_PASSWORD = config("MAIL_PASSWORD")
    BASIC_AUTH_USERNAME = config("INVESTOR_USERNAME")
    BASIC_AUTH_PASSWORD = config("INVESTOR_PASSWORD")
    FLASK_ADMIN_SWATCH = "cerulean"
