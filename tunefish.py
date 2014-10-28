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
    return 'Hello World! These are the bands: <br>' + '<br>' . join([str(band) for band in Band.query.all()])

@app.route('/testband')
def testband():
    b = Band('The Foo Fighters', 'foo@bar.de')
    b.login = 'foo'
    b.name = 'The Foo Fighters'
    b.password = "foobar"
    b.descp = 'The Foo Fighters are the foo'
    b.address = 'Fakestreet 123 in NY'
    b.website = 'foofighters.com'
    db_session.add(b)
    db_session.commit()

    c = Band('LinkinPark', 'linksimPark')
    c.email = 'linkinpark@me.com'
    c.emailConfirmed = True
    c.name = 'Linkin Park'
    c.phone = '010414000240'
    c.youtube_id = 'kXYiU_JCYtU'
    c.descp = 'Linkin Park ist eine im Jahr 1996 in Los Angeles gegründete Band, die zumeist dem Crossover oder Nu Metal zugeordnet wird.'
    c.address = 'Linkin Street, CA 23423'
    c.website = 'linkinpark.com'
    db_session.add(c)
    db_session.commit()

    return 'Band created'


@app.route('/json')
def json():
    return jsonify(
        bandnames=[band.address for band in Band.query.all()]
    )


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
