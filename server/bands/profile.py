# coding=utf-8

from __builtin__ import super

from flask import redirect, url_for
from flask.templating import render_template
from server.ajax import AjaxForm
from server.bands.forms import BandForm, TrackUploadForm, TechriderUploadForm, ImageUploadForm
from server.bands.session_mgmt import RestrictedBandPage

from server.models import Band, db


class Onepager(RestrictedBandPage):
    def get(self):
        band_form = BandForm()
        band_form.set_from_model(self.band)
        return render_template('main.html',
                               band_form=band_form,
                               track_form=TrackUploadForm(),
                               image_form=ImageUploadForm(),
                               techrider_form=TechriderUploadForm())


class Confirm(RestrictedBandPage):
    def get(self, band_id):
        band = Band.query.get_or_404(band_id)
        band.emailConfirmed = True
        db.session.commit()
        return redirect(url_for('bands.profile.index'))


class ProfileUpdate(RestrictedBandPage, AjaxForm):
    def __init__(self):
        super(RestrictedBandPage, self).__init__()
        super(AjaxForm, self).__init__()
        self.form = BandForm()

    def on_submit(self):
        self.form.apply_to_model(self.band)
        db.session.commit()
        return {'check_tab': render_template('check.html')}