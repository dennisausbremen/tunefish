# coding=utf-8
from flask import session, g, request, current_app
from flask.ext.jwt import JWTError

from server.models import User


def identity(payload):
    user_id = payload['identity']
    user = User.query.get(user_id)

    g.user = user
    session['userId'] = user.id

    return user


def jwt_request_handler():
    if 'Authorization' in request.args:
        auth_header_value = request.args['Authorization']
    else:
        auth_header_value = request.headers.get('Authorization', None)

    auth_header_prefix = current_app.config['JWT_AUTH_HEADER_PREFIX']

    if not auth_header_value:
        return

    parts = auth_header_value.split()

    if parts[0].lower() != auth_header_prefix.lower():
        raise JWTError('Invalid JWT header', 'Unsupported authorization type')
    elif len(parts) == 1:
        raise JWTError('Invalid JWT header', 'Token missing')
    elif len(parts) > 2:
        raise JWTError('Invalid JWT header', 'Token contains spaces')

    return parts[1]



def authenticate(username, password):
    username = username.strip()

    user = User.query.filter(User.login == username).first()
    if user and user.password == password:
        return user