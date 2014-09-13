from flask import Flask, jsonify

from server.database import db_session, init_db
from server.bands import bands
from server.models import Band


app = Flask(__name__, static_folder = 'client')
app.debug = True
app.register_blueprint(bands, url_prefix='/bands')
app.secret_key = "this_should_be_way_more_secret_like_urandom.its_only_static_for_debug_reasons"


init_db()

@app.route('/')
def hello_world():
    return 'Hello World! These are the bands: <br>' + '<br>'.join(
        [band.name for band in Band.query.all()])


@app.route('/testband')
def testband():
    b = Band('The Foo Fighters', 'foo@bar.de')
    b.login = 'foo'
    b.password = "foobar"
    b.descp = 'The Foo Fighters are the foo'
    b.address = 'Fakestreet 123 in NY'
    b.website = 'foofighters.com'
    db_session.add(b)
    db_session.commit()
    return 'Band created'


@app.route('/json')
def json():
    return jsonify(
        bannames=[band.password for band in Band.query.all()]
    )


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
