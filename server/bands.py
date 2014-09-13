from flask import Blueprint, request, jsonify, session
from sqlalchemy.exc import IntegrityError

from server.database import db_session

from server.models import Band


BAND_ID = 'band_id'

bands = Blueprint('bands', __name__, template_folder='templates')


@bands.route('/')
def show():
    if BAND_ID in session:
        return Band.query.filter(Band.id == session[BAND_ID]).first().login
    else:
        return 'unkown'


@bands.route('/login', methods=['POST'])
def login():
    if 'login' in request.form and 'password' in request.form:
        login = request.form['login']
        password = request.form['password']
        band = Band.query.filter(Band.login == login).first()
        if band:
            if band.password == password:
                session[BAND_ID] = band.id
                session.modified = True
                result = 'success'
            else:
                result = 'bad_password'
        else:
            result = 'unkown'
    else:
        result = 'data_missing'

    return jsonify(result=result)


@bands.route('/logout')
def logout():
    session.pop(BAND_ID)


@bands.route('/register', methods=['POST'])
def register():
    if 'login' in request.form and 'password' in request.form:
        try:
            band = Band(request.form['login'], request.form['password'])
            db_session.add(band)
            db_session.commit()
            session[BAND_ID] = band.id
            session.modified = True
            result = 'success'
        except IntegrityError as e:
            result = 'already_exists'
    else:
        result = 'data_missing'

    return jsonify(result=result)