# coding=utf-8
from flask import url_for, redirect, jsonify
from flask.templating import render_template
from sqlalchemy import func

from server.models import User, Comment, Vote, db
from server.models import Band
from server.vote.session_mgmt import RestrictedInactiveUserPage, RestrictedModAdminPage, RestrictedUserPage


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

        return render_template('admin/overview.html', bands=bands, users=users, comments=comments)


class VoteStatistics(RestrictedUserPage):
    def get(self):
        return render_template('statistics.html')


class VoteStatisticsJSON(RestrictedUserPage):
    def get(self):
        vote_query = db.session.query(func.day(Vote.timestamp), func.count(Vote.user_id)).filter(func.day(Vote.timestamp) > 1).group_by(Vote.user_id, func.day(Vote.timestamp))
        votes = vote_query.all()

        json_vote = {}
        for vote in votes:
            indicie = str(vote[0])
            if indicie in json_vote:
                voteDict = json_vote[indicie]
                voteDict['user'] += 1
                voteDict['votes'] += vote[1]
            else:
                voteDict = {'user': 1, 'votes': vote[1]}

            json_vote[indicie] = voteDict

        return jsonify(json_vote)


class VotingOverview(RestrictedModAdminPage):
    def get(self):
        users = User.query.all()
        return render_template('users_overview.html', users=users)