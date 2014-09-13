from flask import Flask, jsonify

from database import db_session, init_db
from server.bands import bands
from server.models import Band


app = Flask(__name__)
app.debug = True
app.register_blueprint(bands, url_prefix='/bands')

init_db()

@app.route('/')
def hello_world():
    return 'Hello World! These are the bands: <br>' + '<br>'.join(
        [band.name for band in Band.query.all()])


@app.route('/testband')
def testband():
    b = Band('The Foo Fighters', 'foo3@bar.de')
    b
    b.password = "foo"
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
