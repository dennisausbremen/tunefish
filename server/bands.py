import uuid

from flask import Blueprint, request, jsonify, session
from sqlalchemy.exc import IntegrityError

from server.models import Band, db


BAND_ID = 'band_id'

bands = Blueprint('bands', __name__, template_folder='templates')
ajax_session = {}


@bands.route('/')
def show():
    if BAND_ID in session:
        return Band.query.filter(Band.id == session[BAND_ID]).first_or_404().login
    else:
        return 'unkown'


@bands.route('/login', methods=['POST'])
def login():
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


@bands.route('/logout', methods=['POST'])
def logout():
    auth_token = request.form['auth_token']
    ajax_session.pop(auth_token, None)


@bands.route('/register', methods=['POST'])
def register():
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