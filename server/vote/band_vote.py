# coding=utf-8
import datetime
from flask import flash, url_for, redirect

from flask.templating import render_template

from server.models import Band, State, Comment, db, Vote
from server.vote.forms import CommentForm
from server.vote.session_mgmt import RestrictedUserPage


class BandApp(RestrictedUserPage):
    def get(self):
        return render_template('app.html')


class BandDetails(RestrictedUserPage):
    def get(self, band_id):
        band = Band.query.get(band_id)
        if band:
            comment_form = CommentForm()
            comment_form.band_id.data = band_id
            return render_template('band_view.html', band=band, comment_form=comment_form)
        else:
            flash('Es existiert keine Band mit dieser ID', 'error')
            return redirect(url_for('vote.bands.list'))
