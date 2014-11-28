# coding=utf-8
import uuid

from flask import Blueprint, request, jsonify, session, render_template
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from wtforms import PasswordField, validators, StringField
from flask_wtf import Form


from server.models import Band, db


class RegistrationForm(Form):
    login = StringField('Login', [validators.Length(min=4, max=25)])
    email = StringField('E-Mail Adresse', [validators.Length(min=6, max=35)])
    password = PasswordField('Passwort', [
        validators.Length(min=6),
        validators.EqualTo('confirm', message='Passwörter müssen identisch sein')
    ])
    confirm = PasswordField('Passwort wiederholen')

bands = Blueprint('bands', __name__, template_folder='templates')
ajax_session = {}


class Index(MethodView):
    def get(self):
        regForm = RegistrationForm()
        # todo push regForm
        return render_template('login.html', error=None)



class Register(MethodView):
    def post(self):
        pass


bands.add_url_rule('/', view_func=Index.as_view('foo'))
bands.add_url_rule('/register', view_func=Register.as_view('register'))


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