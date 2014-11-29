# coding=utf-8

from flask import Blueprint, session, redirect, url_for, request
from flask.templating import render_template
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from wtforms import PasswordField, validators, StringField
from flask_wtf import Form
from flask_mail import Message
from app import mailer

from server.models import Band, db


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
    confirm = PasswordField('Passwort wiederholen')


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
                msg = Message("Willkommen %s" % band.login,
                              sender="noreply@vorstrasse-bremen.de",
                              recipients=[band.email],
                              body=u"""Hallo %s,

willkommnen bei der Sommerfest Auswahl. Um deine Bewerbung abschließen zu können, musst du zuerst deine E-Mail
bestätigen. Klick hierzu einfach auf folgenden Link: %s/bands/confim/%d""" % (band.login, request.url_root, band.id))
                mailer.send(msg)
                session['bandId'] = band.id
                return redirect(url_for('bands.profile'))
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
            if band:
                if band.password == loginForm.password.data:
                    session['bandId'] = band.id
                    return redirect(url_for('bands.profile'))
                else:
                    loginForm.password.errors.append("Falsches Passwort")
            else:
                loginForm.login.errors.append("Unbekannter Login")
        return self.render(loginForm, regForm)


class Logout(MethodView):
    def get(self):
        del session['bandId']
        return redirect(url_for('bands.index'))


class Profile(MethodView):
    def get(self):
        band = Band.query.get_or_404(session['bandId'])
        return "welcome band with login %s" % band.login


bands.add_url_rule('/', view_func=Index.as_view('index'))
bands.add_url_rule('/register', view_func=Register.as_view('register'))
bands.add_url_rule('/login', view_func=Login.as_view('login'))
bands.add_url_rule('/logout', view_func=Logout.as_view('logout'))
bands.add_url_rule('/profile', view_func=Profile.as_view('profile'))
