# coding=utf-8
from flask.ext.jwt import JWT

from server import root_blueprint

from server.app import app
from server.bands import band_blueprint
from server.vote import vote_blueprint, track_blueprint

# this file is only for local testing
# in a productive environment this is
# i.e. ~/fcgi-bin/tunefish-beta
from server.vote.jwt import identity, authenticate, jwt_request_handler

jwt = JWT(app, authenticate, identity)
jwt.request_handler(jwt_request_handler)

app.register_blueprint(band_blueprint, url_prefix='/bands')
app.register_blueprint(vote_blueprint, url_prefix='/vote')
app.register_blueprint(track_blueprint, url_prefix='/vote')
app.register_blueprint(root_blueprint, url_prefix='')


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0')
