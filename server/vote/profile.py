# coding=utf-8
from flask import flash, url_for, redirect

from flask.templating import render_template

from server.models import Access
from server.vote.session_mgmt import RestrictedUserPage


class UserIndex(RestrictedUserPage):
    def get(self):
        if self.user.access > Access.INACTIVE:
            return render_template('main_user.html')
        else:
            return render_template('main_inactive.html')


class AdminIndex(RestrictedUserPage):
    def get(self):
        if self.user.is_admin or self.user.is_mod:
            return render_template('admin/overview.html')
        else:
            flash('Du hast hier keinen Zugriff!', 'error')
            return redirect(url_for('vote.home.index'))