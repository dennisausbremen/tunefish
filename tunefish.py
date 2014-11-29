from flask import jsonify
from server.app import app
from server.bands.profile import profile
from server.bands.session import session_mgmt
from server.bands.tracks import tracks
from server.models import Band, db

app.register_blueprint(session_mgmt, url_prefix='/bands')
app.register_blueprint(profile, url_prefix='/bands')
app.register_blueprint(tracks, url_prefix='/bands')


@app.route('/')
def hello_world():
    return 'Hello World! These are the bands: <br>' + '<br>'.join(
        [band.login for band in Band.query.all()])


@app.route('/testband')
def testband():
    b = Band('The Foo Fighters', 'foo@bar.de')
    b.login = 'foo'
    b.password = "foobar"
    b.descp = 'The Foo Fighters are the foo'
    b.city = 'Fakestreet 123 in NY'
    b.website = 'foofighters.com'
    db.session.add(b)
    db.session.commit()
    return 'Band created'


@app.route('/json')
def json():
    return jsonify(
        bannames=[band.login for band in Band.query.all()]
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
