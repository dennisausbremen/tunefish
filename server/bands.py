# coding=utf-8
import uuid

from flask import Blueprint, request, jsonify, session, redirect
from flask.templating import render_template
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from wtforms import PasswordField, validators, StringField
from flask_wtf import Form

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


bands = Blueprint('bands', __name__, template_folder='templates/bands')
ajax_session = {}


class Index(MethodView):
    def render(self, loginForm, regForm):
        return render_template('login.html', loginForm=loginForm, registerForm=regForm)

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
            if band:
                if band.password == loginForm.password.data:
                    return redirect('../json')
                else:
                    loginForm.password.errors.append("Falsches Passwort")
            else:
                loginForm.login.errors.append("Unbekannter Login")
        return self.render(loginForm, regForm)


bands.add_url_rule('/', view_func=Index.as_view('foo'))
bands.add_url_rule('/register', view_func=Register.as_view('register'))
bands.add_url_rule('/login', view_func=Login.as_view('login'))


@bands.route('/login2', methods=['POST'])
def login2():
    auth_token = None
    if 'login' in request.form and 'password' in request.form:
        login = request.form['login']
        password = request.form['password']
        band = Band.query.filter(Band.login == login).first_or_404()
        if band.password == password:
            auth_token = str(uuid.uuid4())
            session[auth_token] = band.id
            result = 'success'
        else:
            result = 'bad_password'
    else:
        result = 'data_missing'

    return jsonify(result=result, auth_token=auth_token)


@bands.route('/logout2', methods=['POST'])
def logout2():
    auth_token = request.form['auth_token']
    ajax_session.pop(auth_token, None)


@bands.route('/register2', methods=['POST'])
def register2():
    auth_token = None
    if 'login' in request.form and 'password' in request.form:
        try:
            band = Band(request.form['login'], request.form['password'])
            db.session.add(band)
            db.session.commit()
            auth_token = str(uuid.uuid4())
            session[auth_token] = band.id
            result = 'success'
        except IntegrityError as e:
            result = 'already_exists'
    else:
        result = 'data_missing'

    return jsonify(result=result, auth_token=auth_token)