from server.app import app
from server.bands.profile import profile
from server.bands.session_mgmt import session_mgmt
from server.bands.tracks import tracks

app.register_blueprint(session_mgmt, url_prefix='/bands')
app.register_blueprint(profile, url_prefix='/bands')
app.register_blueprint(tracks, url_prefix='/bands')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
