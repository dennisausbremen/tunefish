# coding=utf-8
import datetime
from flask import flash, url_for, redirect

from flask.templating import render_template

from server.models import Band, State, Comment, db, Vote
from server.vote.forms import CommentForm
from server.vote.session_mgmt import RestrictedUserPage


class BandList(RestrictedUserPage):
    def get(self):
        bands = Band.query.filter(Band.state == State.IN_VOTE)
        return render_template('band_list.html', bands=bands)


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


class BandVote(RestrictedUserPage):
    def get(self, band_id, vote):
        band = Band.query.get(band_id)
        if band and 0 < vote < 6:
            voting = Vote.query.filter(Vote.band_id == band_id, Vote.user_id == self.user.id).first()
            if not voting:
                voting = Vote()
                voting.user_id = self.user.id
                voting.band_id = band_id
                db.session.add(voting)

            voting.vote = vote
            db.session.commit()
            flash('Vote gespeichert', 'info')
            return redirect(url_for('vote.bands.view', band_id=band_id))
        else:
            flash('Es existiert keine Band mit dieser ID', 'error')
            return redirect(url_for('vote.bands.list'))


class BandCommendAdd(RestrictedUserPage):
    def post(self):
        comment_form = CommentForm()
        if comment_form.validate_on_submit():
            band_id = comment_form.band_id.data
            comment = Comment()
            comment.author_id = self.user.id
            comment.message = comment_form.message.data
            comment.band_id = band_id
            comment.timestamp = datetime.datetime.now()
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('vote.bands.view', band_id=band_id))

