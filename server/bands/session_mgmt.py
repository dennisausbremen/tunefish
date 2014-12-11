# coding=utf-8
from uuid import uuid4

from flask import session, redirect, url_for, flash, g
from flask.templating import render_template
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from server.ajax import AjaxForm, AJAX_FAIL
from server.bands.forms import LoginForm, RegistrationForm
from server.bands.mails import send_registration_mail

from server.models import Band, db, State


class LoginAndRegister(MethodView):
    def __init__(self):
        super(LoginAndRegister, self).__init__()
        self.login_form = LoginForm()
        self.registration_form = RegistrationForm()

    def render(self):
        return render_template('loginAndRegister.html', loginForm=self.login_form, registerForm=self.registration_form)

    def get(self):
        if 'bandId' in session:
            return redirect(url_for('bands.profile.index'))
        else:
            return self.render()


class Register(LoginAndRegister):
    def post(self):
        if self.registration_form.validate_on_submit():
            try:
                band = Band(self.registration_form.login.data, self.registration_form.password.data)
                band.email = self.registration_form.email.data
                band.email_confirmation_token = str(uuid4())
                db.session.add(band)
                db.session.commit()
                send_registration_mail(band)
                session['bandId'] = band.id
                flash('Willkommen Band "%s".' % band.login, 'info')
                return redirect(url_for('bands.profile.index'))
            except IntegrityError:
                self.registration_form.login.errors.append("Eine Band mit diesem Login existiert bereits")
                return self.render()
        return self.render()


class Login(LoginAndRegister):
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


class RestrictedBandPage(MethodView):
    def dispatch_request(self, *args, **kwargs):
        if not 'bandId' in session:
            return redirect(url_for('bands.session.index'))
        else:
            self.band = Band.query.get(session['bandId'])
            if not self.band:
                del session['bandId']
                return redirect(url_for('bands.session.index'))
            else:
                g.band = self.band
                return super(RestrictedBandPage, self).dispatch_request(*args, **kwargs)


class RestrictedBandAjaxForm(RestrictedBandPage, AjaxForm):
    def __init__(self):
        super(RestrictedBandPage, self).__init__()
        super(AjaxForm, self).__init__()

    def post(self):
        if self.band.state != State.NEW:
            return AJAX_FAIL('Die Banddaten können nach dem Abschluss der Bewerbung nicht mehr geändert werden')
        else:
            return super(RestrictedBandAjaxForm, self).post()