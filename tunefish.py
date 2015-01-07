# coding=utf-8
from server import root_blueprint

from server.app import app
from server.bands import band_blueprint
from server.vote import vote_blueprint


app.register_blueprint(band_blueprint, url_prefix='/bands')
app.register_blueprint(vote_blueprint, url_prefix='/vote')
app.register_blueprint(root_blueprint, url_prefix='')


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0')