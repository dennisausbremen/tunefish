# coding=utf-8
from __builtin__ import super

from flask import Blueprint, redirect, url_for
from flask.templating import render_template
from flask.views import MethodView
from server.bands import RestrictedBandPage, AjaxForm
from server.bands.forms import BandForm, TrackUploadForm, TechriderUploadForm, ImageUploadForm

from server.models import Band, db


class JavaScript(MethodView):
    def get(self):
        return render_template('onepager_ajax.js')


class Confirm(RestrictedBandPage):
    def get(self, band_id):
        band = Band.query.get_or_404(band_id)
        band.emailConfirmed = True
        db.session.commit()
        return redirect(url_for('bands.profile.index'))


class Index(RestrictedBandPage):
    def __init__(self):
        super(Index, self).__init__()
        self.band_form = BandForm()
        self.track_form = TrackUploadForm()
        self.image_form = ImageUploadForm()
        self.techrider = TechriderUploadForm()

    def render(self):
        return render_template('main.html',
                               band_form=self.band_form,
                               track_form=self.track_form,
                               image_form=self.image_form,
                               techrider_form=self.techrider
        )

    def get(self):
        self.band_form.set_from_model(self.band)
        return self.render()


class ProfileUpdate(RestrictedBandPage, AjaxForm):
    def __init__(self):
        super(RestrictedBandPage, self).__init__()
        super(AjaxForm, self).__init__()
        self.form = BandForm()

    def on_submit(self):
        self.form.apply_to_model(self.band)
        db.session.commit()
        return {'check_tab': render_template('check.html')}


profile = Blueprint('bands.profile', __name__, template_folder='../../client/views/bands')
profile.add_url_rule('/confirm/<int:band_id>', view_func=Confirm.as_view('confirm'))
profile.add_url_rule('/profile', view_func=Index.as_view('index'), methods=['GET'])
profile.add_url_rule('/profile/band.js', view_func=JavaScript.as_view('bandjs'), methods=['GET'])
profile.add_url_rule('/profile', view_func=ProfileUpdate.as_view('update'), methods=['POST'])