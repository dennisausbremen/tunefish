# coding=utf-8
from flask import flash, url_for, redirect

from flask.templating import render_template

from server.models import Band, State
from server.vote.session_mgmt import RestrictedUserPage


class BandList(RestrictedUserPage):
    def get(self):
        bands = Band.query.filter(Band.state == State.IN_VOTE)
        return render_template('band_list.html', bands=bands)


class BandDetails(RestrictedUserPage):
    def get(self, band_id):
        band = Band.query.get(band_id)
        if band:
            return render_template('band_view.html', band=band)
        else:
            flash('Es existiert keine Band mit dieser ID', 'error')
            return redirect(url_for('vote.bands.list'))