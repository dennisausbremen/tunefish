# coding=utf-8

from flask import Blueprint, session, redirect, url_for
from flask.templating import render_template
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from wtforms import PasswordField, validators, StringField, TextAreaField, FileField
from flask_wtf import Form

from server.models import Band, db, Track


class LoginForm(Form):
    login = StringField('Login', [validators.DataRequired()])
    password = PasswordField('Passwort', [validators.DataRequired()])


class RegistrationForm(Form):
    login = StringField('Login',
                        [validators.Length(min=4, max=25, message="Login muss zwischen 4 und 25 Zeichen lang sein")])
    email = StringField('E-Mail Adresse', [
        validators.Length(min=6, max=35, message=u'Die E-Mail Adresse muss zwischen 6 und 36 Zeichen lang sein.'),
        validators.Email(message=u'Die angegebene E-Mail Adresse ist ungültig.')])
    password = PasswordField('Passwort', [
        validators.Length(min=6, message=u'Das gewählte Passwort muss mindestens 6 Zeichen lang sein.'),
        validators.EqualTo('confirm', message=u'Passwörter müssen identisch sein')
    ])
    confirm = PasswordField('Passwort wiederholen', [validators.EqualTo('password', message='')])


class BandForm(Form):
    descp = TextAreaField('Band-Beschreibung', [validators.Length(min=30)])
    amount_members = StringField('Anzahl Bandmitglieder', [validators.Length(min=1, max=10)])
    website = StringField('Webseite', [validators.Length(min=6)])
    youtube_id = StringField('Youtube VideoID', [validators.Length(min=6)])
    facebook_page = StringField('facebook Seite')
    phone = StringField('Telefon', [validators.Length(min=6)])
    city = StringField('Stadt', [validators.Length(min=3)])

class AudioForm(Form):
    audioFile = FileField('Audiodatei')
    trackname = StringField('Trackname')

bands = Blueprint('bands', __name__, template_folder='../client/views/bands')


class Index(MethodView):
    def render(self, loginForm, regForm):
        return render_template('loginAndRegister.html', loginForm=loginForm, registerForm=regForm)

    def get(self):
        return self.render(LoginForm(), RegistrationForm())


class Register(Index):
    def post(self):
        regForm = RegistrationForm()
        loginForm = LoginForm()
        if regForm.validate_on_submit():
            try:
                band = Band(regForm.login.data, regForm.password.data)
                band.email = regForm.email.data
                db.session.add(band)
                db.session.commit()
                redirect('/')
            except IntegrityError as e:
                regForm.login.errors.append("Eine Band mit diesem Login existiert bereits")
                return self.render(loginForm, regForm)
        return self.render(loginForm, regForm)


class Login(Index):
    def post(self):
        regForm = RegistrationForm()
        loginForm = LoginForm()
        if loginForm.validate_on_submit():
            band = Band.query.filter(Band.login == loginForm.login.data).first()
            if band and band.password == loginForm.password.data:
                session['bandId'] = band.id
                return redirect(url_for('bands.profile'))
            else:
                loginForm.login.errors.append("Unbekannter Login")
                loginForm.password.errors.append("")
        return self.render(loginForm, regForm)


class Logout(MethodView):
    def get(self):
        del session['bandId']
        return redirect(url_for('bands.index'))


class Profile(MethodView):
    def get(self):
        band = Band.query.get(session['bandId'])
        bandForm = BandForm()
        bandForm.descp.data = band.descp
        bandForm.amount_members.data = band.amount_members
        bandForm.website.data = band.website
        bandForm.youtube_id.data = band.youtube_id
        bandForm.facebook_page.data = band.facebook_page
        bandForm.phone.data = band.phone
        bandForm.city.data = band.city
        return render_template('profile.html', bandForm=bandForm)


class ProfileGeneral(Profile):
    def post(self):
        bandForm = BandForm()
        if bandForm.validate_on_submit():
            band = Band.query.get(session['bandId'])
            band.descp = bandForm.descp.data
            band.amount_members = bandForm.amount_members.data
            band.website = bandForm.website.data
            band.youtube_id = bandForm.youtube_id.data
            band.facebook_page = bandForm.facebook_page.data
            band.phone = bandForm.phone.data
            band.city = bandForm.city.data
            db.session.commit()
        return render_template('profile.html', bandForm=bandForm)

class Audio(MethodView):
    def render(self, audioForm):
        tracks = Track.query.filter_by(band_id=session['bandId'])
        return render_template('audio.html', audioForm=audioForm, tracks=tracks)


    def get(self):
        return self.render(AudioForm())


class AudioGeneral(Audio):
    def post(self):
        audioForm = AudioForm()
        if audioForm.validate_on_submit():
            try:
                track = Track()
                track.band_id = session['bandId']
                track.trackname = audioForm.trackname.data
                db.session.add(track)
                db.session.commit()
                return self.render(audioForm)
            except IntegrityError as e:
                audioForm.trackname.errors.append("Fehler")
                return self.render(audioForm)
        return self.render(audioForm)


bands.add_url_rule('/', view_func=Index.as_view('index'))
bands.add_url_rule('/register', view_func=Register.as_view('register'))
bands.add_url_rule('/login', view_func=Login.as_view('login'))
bands.add_url_rule('/logout', view_func=Logout.as_view('logout'))
bands.add_url_rule('/profile', view_func=Profile.as_view('profile'))
bands.add_url_rule('/profileGeneral', view_func=ProfileGeneral.as_view('profileGeneral'))
bands.add_url_rule('/audio', view_func=Audio.as_view('audio'))
bands.add_url_rule('/audioGeneral', view_func=AudioGeneral.as_view('audioGeneral'))