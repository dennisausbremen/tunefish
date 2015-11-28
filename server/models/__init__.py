# coding=utf-8
import datetime
import math
from string import lower

from flask import session, url_for
from flask.ext.images import resized_img_src
from flask.ext.sqlalchemy import SQLAlchemy, iteritems
from markupsafe import Markup
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import URLType, PasswordType

from server.app import app, trackPool, techriderPool, imagePool
from server.bands.forms import BandForm
from server.models.simple_math import average, variance


db = SQLAlchemy(app)


class State:
    NEW = 0
    IN_VOTE = 1
    DECLINED = 2
    ACCEPTED = 3
    OUT_OF_VOTE = 4
    REQUESTED = 5

    descp = {
        NEW: u'Unvollständig',
        IN_VOTE: u'Im Voting',
        DECLINED: u'Abgesagt',
        ACCEPTED: u'Gebucht',
        OUT_OF_VOTE: u'Aus Voting genommen',
        REQUESTED: u'Angefragt'
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
    distance = db.Column(Integer)
    tracks = db.relationship('Track', backref='band', lazy='dynamic')
    comments = db.relationship('Comment', backref='comment', lazy='dynamic')
    votes = db.relationship("Vote", backref="band", order_by="Vote.vote")

    def __init__(self, login, password):
        self.login = login
        self.name = login
        self.password = password

    def __repr__(self):
        return '<Band %r %s>' % (self.name, self.image)

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
        return average(self.votes)

    @property
    def vote_variance(self):
        return variance(self.votes)

    @property
    def vote_count(self):
        return len(self.votes)

    @property
    def vote_with_deviation(self):
        return round(self.vote_average + math.sqrt(self.vote_variance), 2)

    def get_user_vote(self, user):
        vote = [vote.vote for vote in self.votes if vote.user_id == user.id]
        if len(vote) == 0:
            return 0
        else:
            return vote[0]

    def nl2br_desc(self):
        return Markup(self.descp.replace('\n', '<br />\n'))

    @property
    def facebook_url(self):
        if self.facebook_page:
            if 'facebook.com' in self.facebook_page:
                if not self.facebook_page.startswith('http'):
                    return 'https://' + self.facebook_page
                else:
                    return self.facebook_page
            else:
                return 'https://facebook.com/' + self.facebook_page
        else:
            return False

    @property
    def youtube_url(self):
        if self.youtube_id:
            if 'youtube' in self.youtube_id:
                if not self.youtube_id.startswith('http'):
                    return 'https://' + self.youtube_id
                else:
                    return self.youtube_id
            else:
                return 'http://www.youtube.com/embed/' + self.youtube_id
        else:
            return False

    @property
    def prev_image(self):
        if self.image:
            return resized_img_src(self.image, mode="crop", width=1024, quality=60)
        else:
            return False


    @property
    def thumbnail(self):
        if self.image:
            return resized_img_src(self.image, mode="crop", width=200, height=200, quality=60)
        else:
            return False


class Track(db.Model):
    id = db.Column(Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    filename = db.Column(String(80))
    trackname = db.Column(String(100))

    def get_track_url(self):
        # try to fix for stefan by delievering the original mp3
        user_id_stefanbo = 10
        if session['userId'] == user_id_stefanbo:
            return self.url
        else:
            return url_for('track.ajax.track', track_id=self.id)


    def get_track_url_v2(self):
        return url_for('track.api.v2.track', track_id=self.id)


    @property
    def nice_trackname(self):
        # remove whitespace around the string
        track_name = self.trackname.strip()

        # from here on from the beginning:
        # remove starting digits, - and whitespaces
        while track_name[0].isdigit() or track_name.startswith('-'):
            track_name = track_name[1:].strip()

        # remove the band name and whitespaces
        if track_name.lower().startswith(self.band.name.lower()):
            track_name = track_name[len(self.band.name):].strip()

        # remove starting digits, - and whitespaces again
        while track_name[0].isdigit() or track_name.startswith('-'):
            track_name = track_name[1:].strip()

        # let's get from the end
        # remove .mp3
        if track_name.endswith(".mp3"):
            track_name = track_name[:-4]

        # replace underscores through whitespaces
        track_name = track_name.replace('_', ' ').strip()

        return track_name

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
    votes = db.relationship('Vote', backref='user', lazy='dynamic')

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self._access = Access.INACTIVE

    def __repr__(self):
        return '<User %r>' % (self.login)

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

    @property
    def votes_list(self):
        return self.votes.all()

    @property
    def vote_count(self):
        return len(self.votes_list)

    @property
    def vote_average(self):
        return average(self.votes_list)

    @property
    def vote_variance(self):
        return variance(self.votes_list)

    @property
    def vote_latest(self):
        since = datetime.datetime.now() - datetime.timedelta(hours=24)
        return self.votes.filter(Vote.timestamp > since).count()

    def anonymous_login(self):
        return lower(self.login[0]) + '***'


class Vote(db.Model):
    band_id = db.Column(Integer, db.ForeignKey('band.id'), primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('user.id'), primary_key=True)
    vote = db.Column(Integer)
    timestamp = db.Column(DateTime)

    def __init__(self):
        self.timestamp = datetime.datetime.now()


class Comment(db.Model):
    id = db.Column(Integer, primary_key=True)
    band_id = db.Column(Integer, db.ForeignKey('band.id'))
    band = db.relationship("Band", backref=db.backref("comment", uselist=False))
    author_id = db.Column(Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", backref=db.backref("comment", uselist=False))

    message = db.Column(String(1000))
    timestamp = db.Column(DateTime)

    def __init__(self):
        self.timestamp = datetime.datetime.now()

    @property
    def date_time(self):
        return self.timestamp.strftime("%d.%m.%y - %H:%M")


class Reminder(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(60))
    email = db.Column(String(100))
    register_time = db.Column(DateTime)

    def __init__(self):
        self.register_time = datetime.datetime.now()

db.create_all()