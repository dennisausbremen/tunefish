# coding=utf-8
from flask import url_for, redirect

from flask.templating import render_template

from server.vote.session_mgmt import RestrictedInactiveUserPage, RestrictedModAdminPage


class InactiveUserIndex(RestrictedInactiveUserPage):
    def get(self):
        if self.user.is_inactive:
            return render_template('main_inactive.html')
        else:
            return redirect(url_for('vote.bands.app'))


class AdminIndex(RestrictedModAdminPage):
    def get(self):
        return render_template('admin/overview.html')