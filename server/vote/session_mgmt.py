# coding=utf-8
from flask import session, redirect, url_for, flash, g
from flask.templating import render_template
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from server.ajax import AjaxForm
from server.bands.forms import LoginForm
from server.models import db, User
from server.vote.forms import UserRegistrationForm


class LoginAndRegisterUser(MethodView):
    def __init__(self):
        super(LoginAndRegisterUser, self).__init__()
        self.login_form = LoginForm()
        self.registration_form = UserRegistrationForm()

    def render(self):
        return render_template('loginAndRegisterUser.html', loginForm=self.login_form, registerForm=self.registration_form)

    def get(self):
        if 'userId' in session:
            return redirect(url_for('vote.home.index'))
        else:
            return self.render()


class RegisterUser(LoginAndRegisterUser):
    def post(self):
        if self.registration_form.validate_on_submit():
            try:
                user = User(self.registration_form.login.data, self.registration_form.password.data)
                db.session.add(user)
                db.session.commit()
                session['userId'] = user.id
                flash('Willkommen Benutzer "%s".' % user.login, 'info')
                return redirect(url_for('vote.home.index'))
            except IntegrityError:
                self.registration_form.login.errors.append("Eine Band mit diesem Login existiert bereits")
                return self.render()
        return self.render()


class LoginUser(LoginAndRegisterUser):
    def post(self):
        if self.login_form.validate_on_submit():
            user = User.query.filter(User.login == self.login_form.login.data).first()
            if user and user.password == self.login_form.password.data:
                session['userId'] = user.id
                return redirect(url_for('vote.home.index'))
            else:
                self.login_form.login.errors.append(u'Bitte überprüfe deine Eingaben')
                self.login_form.password.errors.append("Passwort eingeben")
        return self.render()


class LogoutUser(MethodView):
    def get(self):
        try:
            del session['userId']
        finally:
            return redirect(url_for('vote.session.index'))


class RestrictedUserPage(MethodView):
    def dispatch_request(self, *args, **kwargs):
        if not 'userId' in session:
            return redirect(url_for('vote.session.index'))
        else:
            self.user = User.query.get(session['userId'])
            if not self.user:
                del session['userId']
                return redirect(url_for('vote.session.index'))
            else:
                g.user = self.user
                return super(RestrictedUserPage, self).dispatch_request(*args, **kwargs)


class RestrictedUserAjaxForm(RestrictedUserPage, AjaxForm):
    def __init__(self):
        super(RestrictedUserPage, self).__init__()
        super(AjaxForm, self).__init__()

    def post(self):
        return super(RestrictedUserAjaxForm, self).post()