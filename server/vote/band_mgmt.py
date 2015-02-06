# coding=utf-8
from flask import flash, url_for, redirect
from flask.templating import render_template

from server.models import Band, State, db
from server.vote.session_mgmt import RestrictedModAdminPage


class AdminBandList(RestrictedModAdminPage):
    def get(self):
        bands = Band.query.all()
        return render_template('admin/band_list.html', bands=bands)


class AdminBandView(RestrictedModAdminPage):
    def get(self, band_id):
        band = Band.query.get(band_id)
        if band:
            return render_template('admin/band_view.html', band=band)
        else:
            flash('Es existiert keine Band mit dieser ID', 'error')
            return redirect(url_for('vote.admin.bands.list'))


class AdminBandState(RestrictedModAdminPage):
    def get(self, band_id):
        band = Band.query.get(band_id)
        if band:
            if band.state == State.IN_VOTE:
                band.state = State.OUT_OF_VOTE
                flash('Band aus dem Voting genommen', 'info')
            else:
                band.state = State.IN_VOTE
                flash('Band wieder in das Voting aufgenommen', 'info')
            db.session.commit()
            return redirect(url_for('vote.admin.bands.list'))
        else:
            flash('Es existiert keine Band mit dieser ID', 'error')
            return redirect(url_for('vote.admin.bands.list'))