# coding=utf-8
from flask import session, redirect, url_for, flash, g, request
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
        return render_template('loginAndRegisterUser.html', loginForm=self.login_form,
                               registerForm=self.registration_form)

    def get(self):
        if 'userId' in session:
            return redirect(url_for('vote.bands.app', _anchor='/bands'))
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
                return redirect(url_for('vote.home.inactive'))
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
                if user.is_inactive:
                    return redirect(url_for('vote.home.inactive'))
                else:
                    return redirect(url_for('vote.bands.app', _anchor='/bands'))
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


class RestrictedInactiveUserPage(MethodView):
    def initialize_user(self):
        if not 'userId' in session:
            return False
        else:
            self.user = User.query.get(session['userId'])
            if not self.user:
                del session['userId']
                return False
            else:
                return True

    def redirect_to_login(self):
        return redirect(url_for('vote.session.index'))

    def dispatch_request(self, *args, **kwargs):
        if self.initialize_user():
            g.user = self.user
            return super(RestrictedInactiveUserPage, self).dispatch_request(*args, **kwargs)
        else:
            return self.redirect_to_login()


class RestrictedUserPage(RestrictedInactiveUserPage):
    def dispatch_request(self, *args, **kwargs):
        if self.initialize_user():
            g.user = self.user
            if self.user.is_inactive:
                return redirect(url_for('vote.home.inactive'))
            else:
                return super(RestrictedUserPage, self).dispatch_request(*args, **kwargs)
        else:
            return self.redirect_to_login()


class RestrictedModAdminPage(RestrictedUserPage):
    def dispatch_request(self, *args, **kwargs):
        if self.initialize_user() and (self.user.is_admin or self.user.is_mod):
            return super(RestrictedModAdminPage, self).dispatch_request(*args, **kwargs)
        else:
            flash('Du hast hier keinen Zugriff.', 'error')
            return redirect(url_for('vote.bands.app', _anchor='/bands'))


class RestrictedAdminPage(RestrictedUserPage):
    def dispatch_request(self, *args, **kwargs):
        if self.initialize_user() and self.user.is_admin:
            return super(RestrictedAdminPage, self).dispatch_request(*args, **kwargs)
        else:
            flash('Du hast hier keinen Zugriff.', 'error')
            return redirect(url_for('vote.bands.app', _anchor='/bands'))


class RestrictedUserAjaxForm(RestrictedUserPage, AjaxForm):
    def __init__(self):
        super(RestrictedUserPage, self).__init__()
        super(AjaxForm, self).__init__()

    def post(self):
        return super(RestrictedUserAjaxForm, self).post()