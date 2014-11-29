# coding=utf-8
from __builtin__ import super

from flask import Blueprint, session, redirect, url_for
from flask.templating import render_template
from flask.views import MethodView
from server.bands.forms import BandForm

from server.models import Band, db


profile = Blueprint('bands.profile', __name__, template_folder='../../client/views/bands')


class RestrictedBandPage(MethodView):
    def dispatch_request(self, *args, **kwargs):
        if not 'bandId' in session:
            return redirect(url_for('bands.session.index'))
        else:
            self.band = Band.query.get(session['bandId'])
            if not self.band:
                return redirect(url_for('bands.session.index'))
            else:
                return super(RestrictedBandPage, self).dispatch_request(*args, **kwargs)


class Confirm(RestrictedBandPage):
    def get(self, band_id):
        band = Band.query.get_or_404(band_id)
        band.emailConfirmed = True
        db.session.commit()
        return redirect(url_for('bands.session.profile'))


class ProfilePage(RestrictedBandPage):
    def __init__(self):
        super(ProfilePage, self).__init__()
        self.form = BandForm()

    def render(self):
        return render_template('profile.html', bandForm=self.form)

    def get(self):
        self.form.set_from_model(self.band)
        return self.render()


class ProfileGeneral(ProfilePage):
    def post(self):
        if self.form.validate_on_submit():
            self.form.apply_to_model(self.band)
            db.session.commit()
        return self.render()


profile.add_url_rule('/confirm/<int:band_id>', view_func=Confirm.as_view('confirm'))
profile.add_url_rule('/profile', view_func=ProfilePage.as_view('profile'))
profile.add_url_rule('/profileGeneral', view_func=ProfileGeneral.as_view('profileGeneral'))