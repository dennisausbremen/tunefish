# coding=utf-8
from flask import session
from flask.ext.sqlalchemy import SQLAlchemy, iteritems
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import URLType, PasswordType

from server.app import app, trackPool, techriderPool, imagePool
from server.bands.forms import BandForm


db = SQLAlchemy(app)


class State:
    NEW = 0
    IN_VOTE = 1
    DECLINED = 2
    ACCEPTED = 3

    descp = {
        NEW: u'Unvollständig',
        IN_VOTE: u'Im Voting',
        DECLINED: u'Abgelehnt',
        ACCEPTED: u'Voting bestanden'
    }


class Access:
    INACTIVE = 0
    USER = 1
    MODERATOR = 2
    ADMIN = 3


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
    comments = db.relationship('Comment', backref='comment', lazy='dynamic')
    votes = db.relationship("Vote", backref="band")



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


    @property
    def state_label(self):
        return State.descp[self.state]

    @property
    def vote_average(self):
        if self.vote_count == 0:
            return 0
        else:
            return sum([x.vote for x in self.votes]) / float(len(self.votes))

    @property
    def vote_count(self):
        return len(self.votes)

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


class User(db.Model):
    id = db.Column(Integer, primary_key=True)
    login = db.Column(String(25), unique=True)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']))
    name = db.Column(String(60))
    _access = db.Column(Integer)

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self._access = Access.INACTIVE

    def __repr__(self):
        return '<User %r>' % (self.name)

    @hybrid_property
    def access(self):
        return self._access

    # avoid disallowed changes
    @access.setter
    def access(self, access):
        cur_user = User.query.get(session['userId'])

        if cur_user and cur_user.access >= access:
            self._access = access

    @property
    def access_name(self):
        access_names = {0: 'Inaktiv', 1: 'Benutzer', 2: 'Moderator', 3: 'Administrator'}
        return access_names[self.access]

    @property
    def is_inactive(self):
        return self.access == Access.INACTIVE

    @property
    def is_mod(self):
        return self.access == Access.MODERATOR

    @property
    def is_admin(self):
        return self.access == Access.ADMIN

    @property
    def is_user(self):
        return self.access == Access.USER


class Vote(db.Model):
    band_id = db.Column(Integer, db.ForeignKey('band.id'), primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('user.id'), primary_key=True)
    vote = db.Column(Integer)

class Comment(db.Model):
    id = db.Column(Integer, primary_key=True)
    band_id = db.Column(Integer, db.ForeignKey('band.id'))
    author_id = db.Column(Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", backref=db.backref("comment", uselist=False))

    message = db.Column(String(1000))
    timestamp = db.Column(DateTime)


db.create_all()