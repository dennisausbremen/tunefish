from flask import Flask

from database import db_session, init_db
from server.models import Band


app = Flask(__name__)
app.debug = True

init_db()

@app.route('/')
def hello_world():
    return 'Hello World! These are the bands: <br>' + '<br>'.join(
        [band.name for band in Band.query.all()])


@app.route('/testband')
def testband():
    b = Band('The Foo Fighters', 'foo2@bar.de')
    db_session.add(b)
    db_session.commit()
    return 'Band created'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()
