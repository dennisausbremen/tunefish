# coding=utf-8
from flask.templating import render_template

from server.vote.session_mgmt import RestrictedUserPage


class BandApp(RestrictedUserPage):
    def get(self):
        return render_template('app.html')


class AngularApp(RestrictedUserPage):
    def get(self):
        return render_template('angular.html')