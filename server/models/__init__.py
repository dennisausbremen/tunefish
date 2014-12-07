from flask.ext.sqlalchemy import SQLAlchemy, iteritems
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy_utils import URLType, PasswordType

from server.app import app, trackPool, techriderPool, imagePool
from server.bands.forms import BandForm


db = SQLAlchemy(app)


class Band(db.Model):
    id = db.Column(Integer, primary_key=True)
    login = db.Column(String, unique=True)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']))
    name = db.Column(String)
    email = db.Column(String)
    is_email_confirmed = db.Column(Boolean, default=False)
    email_confirmation_token = db.Column(String)
    descp = db.Column(String)
    amount_members = db.Column(String)
    website = db.Column(URLType)
    youtube_id = db.Column(String)
    facebook_page = db.Column(String)
    phone = db.Column(String)
    city = db.Column(String)
    image = db.Column(String)
    techrider = db.Column(String)
    state = db.Column(Integer)
    apply_timestamp = db.Column(DateTime)
    tracks = db.relationship('Track', backref='band', lazy='dynamic')

    def __init__(self, login, password):
        self.login = login
        self.name = login
        self.password = password

    def __repr__(self):
        return '<Band %r>' % (self.name)

    @property
    def is_tracks_valid(self):
        return 2 < self.tracks.count() < 6

    @property
    def is_profile_valid(self):
        bandForm = BandForm()
        bandForm.set_from_model(self)

        for name, field in iteritems(bandForm._fields):
            if not field.validate(self, []):
                return False
        return True


    @property
    def techrider_url(self):
        return techriderPool.url(self.techrider)

    @property
    def techrider_path(self):
        return techriderPool.path(self.techrider)

    @property
    def image_url(self):
        return imagePool.url(self.image)

    @property
    def image_path(self):
        return imagePool.path(self.image)


class Track(db.Model):
    id = db.Column(Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    filename = db.Column(String)
    trackname = db.Column(String)

    @property
    def url(self):
        return trackPool.url(self.filename)

    @property
    def path(self):
        return trackPool.path(self.filename)


db.create_all()