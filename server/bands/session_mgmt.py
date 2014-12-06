# coding=utf-8

from flask import Blueprint, session, redirect, url_for, request, flash, jsonify
from flask.templating import render_template
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from flask_mail import Message
from server.app import mailer
from server.bands.forms import LoginForm, RegistrationForm

from server.models import Band, db

MAIL_BODY = u"""Hallo %s,


willkommnen bei der Sommerfest Auswahl. Um deine Bewerbung abschließen zu können, musst du zuerst deine E-Mail
bestätigen. Klick hierzu einfach auf folgenden Link: %sbands/confirm/%d


Viele Grüße
SoFe Orga '15
"""


class Index(MethodView):
    def __init__(self):
        super(Index, self).__init__()
        self.login_form = LoginForm()
        self.registration_form = RegistrationForm()

    def render(self):
        return render_template('loginAndRegister.html', loginForm=self.login_form, registerForm=self.registration_form)

    def get(self):
        if 'bandId' in session:
            return redirect(url_for('bands.profile.index'))
        else:
            return self.render()


class Register(Index):
    def post(self):
        if self.registration_form.validate_on_submit():
            try:
                band = Band(self.registration_form.login.data, self.registration_form.password.data)
                band.email = self.registration_form.email.data
                db.session.add(band)
                db.session.commit()
                msg = Message("Willkommen %s" % band.login,
                              sender="noreply@vorstrasse-bremen.de",
                              recipients=[band.email],
                              body=MAIL_BODY % (band.login, request.url_root, band.id))
                mailer.send(msg)
                session['bandId'] = band.id
                flash('Willkommen Band "%s".' % band.login, 'info')
                return redirect(url_for('bands.profile.index'))
            except IntegrityError as e:
                self.registration_form.login.errors.append("Eine Band mit diesem Login existiert bereits")
                return self.render()
        return self.render()


class Login(Index):
    def post(self):
        if self.login_form.validate_on_submit():
            band = Band.query.filter(Band.login == self.login_form.login.data).first()
            if band and band.password == self.login_form.password.data:
                session['bandId'] = band.id
                return redirect(url_for('bands.profile.index'))
            else:
                self.login_form.login.errors.append(u'Bitte überprüfe deine Eingaben')
                self.login_form.password.errors.append("Passwort eingeben")
        return self.render()

class Logout(MethodView):
    def get(self):
        try:
            del session['bandId']
        finally:
            return redirect(url_for('bands.session.index'))



session_mgmt = Blueprint('bands.session', __name__, template_folder='../../client/views/bands')
session_mgmt.add_url_rule('/', view_func=Index.as_view('index'), methods=['GET'])
session_mgmt.add_url_rule('/', view_func=Login.as_view('login'), methods=['POST'])
session_mgmt.add_url_rule('/register', view_func=Register.as_view('register'))
session_mgmt.add_url_rule('/logout', view_func=Logout.as_view('logout'))