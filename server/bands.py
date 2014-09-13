from flask import Blueprint, request, jsonify, session
from sqlalchemy.exc import IntegrityError

from server.database import db_session

from server.models import Band


BAND_ID = 'band_id'

bands = Blueprint('bands', __name__, template_folder='templates')

@bands.route('/', defaults={'id': 1})
@bands.route('/<id>')
def show(id):
    return Band.query.filter(Band.id == id).first().name


@bands.route('/login', methods=['POST'])
def login():
    login = request.args.get('login', None, type=str)  # todo normalize
    password = request.args.get('password', None, type=str)
    if login and password:
        band = Band.query.filter(Band.login == 'login').first()
        if band:
            if band.password == password:
                result = 'success'
                session[BAND_ID] = band.id
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
    login = request.args.get('login', None, type=str)  # todo normalize
    password = request.args.get('password', None, type=str)
    if login and password:
        try:
            db_session.add(Band(login, password))
            db_session.commit()
            result = 'success'
        except IntegrityError as e:
            result = 'already_exists'
    return jsonify(result=result)