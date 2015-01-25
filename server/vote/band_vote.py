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