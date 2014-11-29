# coding=utf-8

from flask import Blueprint, session, redirect, url_for, request
from flask.templating import render_template
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from flask_mail import Message
from server.app import mailer
from server.bands.forms import LoginForm, RegistrationForm

from server.models import Band, db


session_mgmt = Blueprint('bands.session', __name__, template_folder='../../client/views/bands')


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
bestätigen. Klick hierzu einfach auf folgenden Link: %sbands/confirm/%d""" % (band.login, request.url_root, band.id))
                mailer.send(msg)
                session['bandId'] = band.id
                return redirect(url_for('bands.session.profile'))
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
                return redirect(url_for('bands.profile.profile'))
            else:
                loginForm.login.errors.append("Unbekannter Login")
                loginForm.password.errors.append("")
        return self.render(loginForm, regForm)


class Logout(MethodView):
    def get(self):
        del session['bandId']
        return redirect(url_for('bands.session.index'))


session_mgmt.add_url_rule('/', view_func=Index.as_view('index'))
session_mgmt.add_url_rule('/register', view_func=Register.as_view('register'))
session_mgmt.add_url_rule('/login', view_func=Login.as_view('login'))
session_mgmt.add_url_rule('/logout', view_func=Logout.as_view('logout'))