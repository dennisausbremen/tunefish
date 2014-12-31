# coding=utf-8

from flask import Blueprint, render_template
from flask.views import MethodView
from server.bands.image import ImageUpload
from server.bands.profile import Confirm, ProfileUpdate, Onepager, ResendConfirmMail, SubmitProfile
from server.bands.session_mgmt import LoginAndRegister, Login, Register, Logout
from server.bands.techrider import TechriderUpload
from server.bands.tracks import TrackUpload, TrackDelete


class JavaScript(MethodView):
    def get(self):
        return render_template('onepager_ajax.js')


band_blueprint = Blueprint('bands', __name__, template_folder='../../client/views/bands')

band_blueprint.add_url_rule('/', view_func=LoginAndRegister.as_view('session.index'), methods=['GET'])
band_blueprint.add_url_rule('/', view_func=Login.as_view('session.login'), methods=['POST'])
band_blueprint.add_url_rule('/register', view_func=Register.as_view('session.register'))
band_blueprint.add_url_rule('/logout', view_func=Logout.as_view('session.logout'))

band_blueprint.add_url_rule('/confirm/<string:token>', view_func=Confirm.as_view('profile.confirm'))
band_blueprint.add_url_rule('/submit', view_func=SubmitProfile.as_view('profile.submit'))
band_blueprint.add_url_rule('/resend-confirm', view_func=ResendConfirmMail.as_view('profile.resend'))
band_blueprint.add_url_rule('/profile', view_func=Onepager.as_view('profile.index'), methods=['GET'])
band_blueprint.add_url_rule('/profile', view_func=ProfileUpdate.as_view('profile.update'), methods=['POST'])
# band_blueprint.add_url_rule('/profile.js', view_func=JavaScript.as_view('profile.bandjs'), methods=['GET'])

band_blueprint.add_url_rule('/images', view_func=ImageUpload.as_view('image.upload'))
band_blueprint.add_url_rule('/techrider', view_func=TechriderUpload.as_view('techrider.upload'))

band_blueprint.add_url_rule('/tracks', view_func=TrackUpload.as_view('tracks.upload'))
band_blueprint.add_url_rule('/tracks/delete/<int:track_id>', view_func=TrackDelete.as_view('tracks.delete'))