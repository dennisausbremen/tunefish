# coding=utf-8

from server.app import app
from server.bands import band_blueprint


app.register_blueprint(band_blueprint, url_prefix='/bands')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
