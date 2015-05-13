# coding=utf-8

from __builtin__ import super
from datetime import datetime

from flask import redirect, url_for, Response, flash
from flask.templating import render_template
from flask.views import MethodView
from server import app
from server.bands.forms import BandForm, TrackUploadForm, TechriderUploadForm, ImageUploadForm
from server.bands.mails import send_registration_mail
from server.bands.session_mgmt import RestrictedBandPage, RestrictedBandAjaxForm

from server.models import Band, db, State, Reminder


class Onepager(RestrictedBandPage):
    def get(self):
        if datetime.strptime(app.SETTINGS['BAND_CANDIDATURE_END'], "%Y-%m-%d %H:%M:%S") < datetime.now():
            return render_template('main_after_deadline.html', states=State)
        else:
            if self.band.state == State.NEW:
                band_form = BandForm()
                band_form.set_from_model(self.band)
                return render_template('main.html',
                                       band_form=band_form,
                                       track_form=TrackUploadForm(),
                                       image_form=ImageUploadForm(),
                                       techrider_form=TechriderUploadForm())
            else:
                return render_template('main_after_submit.html')


class RegisterReminder(MethodView):
    def get(self, token):
        band = Band.query_or_404.filter(Band.email_confirmation_token[:15] == token).first()
        if band:
            reminder = Reminder()
            reminder.email = band.email
            reminder.name = band.name

            db.session.add(reminder)
            db.session.commit()

            flash('success', 'Erfolgreich für die Benachrichtigung 2016 angemeldet.')
            return redirect('bands.session.index')


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


class SubmitProfile(RestrictedBandPage):
    def get(self):
        if datetime.strptime(app.SETTINGS['BAND_CANDIDATURE_END'], "%Y-%m-%d %H:%M:%S") < datetime.now():
            flash(u'Die Bestätigung der Bewerbung ist nicht mehr möglich!', 'error')
        else:
            if self.band.is_ready_for_submit:
                self.band.state = State.IN_VOTE
                db.session.commit()
                flash(u'Anmeldung erfolgreich', 'info')
            else:
                flash(u'Die Daten für die Anmeldung sind unvollständig', 'error')
        return redirect(url_for('bands.profile.index'))
