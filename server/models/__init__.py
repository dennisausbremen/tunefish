from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import PasswordType

from server.database import db_session


Base = declarative_base()
Base.query = db_session.query_property()


class Band(Base):
    __tablename__ = 'bands'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']))

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Band %r>' % (self.name)