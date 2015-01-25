# coding=utf-8
from flask import flash, url_for, redirect

from flask.templating import render_template

from server.models import Access
from server.vote.session_mgmt import RestrictedUserPage, RestrictedInactiveUserPage


class InactiveUserIndex(RestrictedInactiveUserPage):
    def get(self):
        if self.user.is_inactive:
            return render_template('main_inactive.html')
        else:
            return redirect(url_for('vote.bands.app'))


class AdminIndex(RestrictedUserPage):
    def get(self):
        if self.user.is_admin or self.user.is_mod:
            return render_template('admin/overview.html')
        else:
            flash('Du hast hier keinen Zugriff!', 'error')
            return redirect(url_for('vote.bands.app'))