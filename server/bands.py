from flask import Blueprint, request, jsonify, session

from server.models import Band


bands = Blueprint('bands', __name__, template_folder='templates')


@bands.route('/', defaults={'id': 1})
@bands.route('/<id>')
def show(id):
    return Band.query.filter(Band.id == id).first().name


@bands.route('/login', methods=['POST'])
def login():
    login = request.args.get('login', None, type=str)
    password = request.args.get('password', None, type=str)
    if login and password:
        band = Band.query.filter(Band.login == 'login').first()
        if band:
            if band.password == password:
                result = 'success'
                session['band_id'] = band.id
            else:
                result = 'bad_password'
        else:
            result = 'unkown'
    else:
        result = 'data_missing'

    return jsonify(result=result)

