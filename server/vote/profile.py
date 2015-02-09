# coding=utf-8
from flask import url_for, redirect

from flask.templating import render_template
from server.models import User, Comment
from server.models import Band

from server.vote.session_mgmt import RestrictedInactiveUserPage, RestrictedModAdminPage


class InactiveUserIndex(RestrictedInactiveUserPage):
    def get(self):
        if self.user.is_inactive:
            return render_template('main_inactive.html')
        else:
            return redirect(url_for('vote.bands.app'))


class AdminIndex(RestrictedModAdminPage):
    def get(self):
        bands = Band.query.all()
        users = User.query.all()
        comments = Comment.query.order_by(Comment.timestamp.desc()).all()

        return render_template('admin/overview.html', bands=bands, users=users, comments=comments )