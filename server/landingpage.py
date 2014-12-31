# coding=utf-8

from __builtin__ import super

from flask import redirect, url_for, Response, flash
from flask.templating import render_template
from flask.views import MethodView
from server.bands.forms import BandForm, TrackUploadForm, TechriderUploadForm, ImageUploadForm
from server.bands.mails import send_registration_mail
from server.bands.session_mgmt import RestrictedBandPage, RestrictedBandAjaxForm

from server.models import Band, db, State


class LandingPage(MethodView):
    def get(self):
        return render_template('landingpage.html')