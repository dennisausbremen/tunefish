from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy_utils import PasswordType, URLType

from server.database import db_session


Base = declarative_base()
Base.query = db_session.query_property()


class Band(Base):
    __tablename__ = 'bands'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    emailConfirmed = Column(Boolean, default=False)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']))
    descp = Column(String)
    website = Column(URLType)
    youtube_id = Column(String)
    phone = Column(String)
    address = Column(String)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Band %r>' % (self.name)