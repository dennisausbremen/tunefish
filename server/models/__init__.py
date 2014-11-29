from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from sqlalchemy_utils import URLType, PasswordType

from server.app import app


db = SQLAlchemy(app)


class Band(db.Model):
    id = db.Column(Integer, primary_key=True)
    login = db.Column(String, unique=True)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']))
    name = db.Column(String)
    email = db.Column(String)
    emailConfirmed = db.Column(Boolean, default=False)
    descp = db.Column(String)
    amount_members = db.Column(String)
    website = db.Column(URLType)
    youtube_id = db.Column(String)
    facebook_page = db.Column(String)
    phone = db.Column(String)
    city = db.Column(String)


    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return '<Band %r>' % (self.name)


db.create_all()