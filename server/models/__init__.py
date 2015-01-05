from flask.ext.sqlalchemy import SQLAlchemy, iteritems
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy_utils import URLType, PasswordType

from server.app import app, trackPool, techriderPool, imagePool
from server.bands.forms import BandForm


db = SQLAlchemy(app)


class State:
    NEW = 0
    READY_FOR_VOTE = 1
    IN_VOTE = 2
    DECLINED = 3
    ACCEPTED = 4


class Band(db.Model):
    id = db.Column(Integer, primary_key=True)
    login = db.Column(String(25), unique=True)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']))
    name = db.Column(String(60))
    email = db.Column(String(100))
    is_email_confirmed = db.Column(Boolean, default=False)
    email_confirmation_token = db.Column(String(36))
    descp = db.Column(String(5000))
    amount_members = db.Column(Integer)
    website = db.Column(URLType)
    youtube_id = db.Column(String(20))
    facebook_page = db.Column(String(100))
    phone = db.Column(String(30))
    city = db.Column(String(50))
    image = db.Column(String(80))
    techrider = db.Column(String(80))
    state = db.Column(Integer, default=State.NEW)
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
        band_form = BandForm()
        band_form.set_from_model(self)

        for field_name, field in iteritems(band_form._fields):
            if not field.validate(self):
                return False
        return True


    @property
    def techrider_url(self):
        if self.techrider:
            return techriderPool.url(self.techrider)
        else:
            return False

    @property
    def techrider_path(self):
        return techriderPool.path(self.techrider)

    @property
    def image_url(self):
        if self.image:
            return imagePool.url(self.image)
        else:
            return False

    @property
    def image_path(self):
        return imagePool.path(self.image)

    @property
    def is_ready_for_submit(self):
        return self.image and \
            self.techrider and \
            self.is_email_confirmed and \
            self.is_profile_valid and \
            self.is_tracks_valid


class Track(db.Model):
    id = db.Column(Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    filename = db.Column(String(80))
    trackname = db.Column(String(100))

    @property
    def url(self):
        return trackPool.url(self.filename)

    @property
    def path(self):
        return trackPool.path(self.filename)


db.create_all()