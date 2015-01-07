# coding=utf-8
from flask import flash, url_for, redirect

from flask.templating import render_template

from server.models import Access, Band, State
from server.vote.session_mgmt import RestrictedUserPage


class AdminBandList(RestrictedUserPage):
    def get(self):
        if self.user.is_mod or self.user.is_admin:
            bands = Band.query.all()
            return render_template('admin/band_list.html', bands=bands, state=State)
        else:
            flash('Du hast hier keinen Zugriff', 'error')
            return redirect(url_for('vote.home.index'))


class AdminBandView(RestrictedUserPage):
    def get(self, band_id):
        if self.user.is_mod or self.user.is_admin:
            band = Band.query.get(band_id)
            if band:
                return render_template('admin/band_view.html', band=band, state=State)
            else:
                flash('Es existiert keine Band mit dieser ID', 'error')
                return redirect(url_for('vote.admin.bands.list'))

        else:
            flash('Du hast hier keinen Zugriff', 'error')
            return redirect(url_for('vote.home.index'))