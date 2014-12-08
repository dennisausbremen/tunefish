# coding=utf-8

from __builtin__ import super

from flask import redirect, url_for, Response, flash
from flask.templating import render_template
from server.bands.forms import BandForm, TrackUploadForm, TechriderUploadForm, ImageUploadForm
from server.bands.mails import send_registration_mail
from server.bands.session_mgmt import RestrictedBandPage, RestrictedBandAjaxForm

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
    def get(self, token):
        band = Band.query.filter(Band.email_confirmation_token == token).first()
        if band:
            band.is_email_confirmed = True
            db.session.commit()
            return redirect(url_for('bands.profile.index'))
        else:
            return Response(404)


class ResendConfirmMail(RestrictedBandPage):
    def get(self):
        send_registration_mail(self.band)
        flash(u'Bestätigungsemail wird versendet', 'info')
        return redirect(url_for('bands.profile.index'))


class ProfileUpdate(RestrictedBandAjaxForm):
    def __init__(self):
        super(RestrictedBandAjaxForm, self).__init__()
        self.form = BandForm()

    def on_submit(self):
        self.form.apply_to_model(self.band)
        db.session.commit()
        return {'check_tab': render_template('check.html')}