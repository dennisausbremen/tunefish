# coding=utf-8
from __builtin__ import super

from flask import Blueprint, redirect, url_for
from flask.templating import render_template
from server.bands import RestrictedBandPage
from server.bands.forms import BandForm

from server.models import Band, db


class Confirm(RestrictedBandPage):
    def get(self, band_id):
        band = Band.query.get_or_404(band_id)
        band.emailConfirmed = True
        db.session.commit()
        return redirect(url_for('bands.profile.index'))


class Index(RestrictedBandPage):
    def __init__(self):
        super(Index, self).__init__()
        self.form = BandForm()

    def render(self):
        return render_template('profile.html', bandForm=self.form)

    def get(self):
        self.form.set_from_model(self.band)
        return self.render()


class ProfileUpdate(Index):
    def post(self):
        if self.form.validate_on_submit():
            self.form.apply_to_model(self.band)
            db.session.commit()
        return self.render()


profile = Blueprint('bands.profile', __name__, template_folder='../../client/views/bands')
profile.add_url_rule('/confirm/<int:band_id>', view_func=Confirm.as_view('confirm'))
profile.add_url_rule('/profile', view_func=Index.as_view('index'), methods=['GET'])
profile.add_url_rule('/profile', view_func=ProfileUpdate.as_view('update'), methods=['POST'])