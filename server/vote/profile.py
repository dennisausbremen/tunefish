# coding=utf-8
from flask import url_for, redirect, jsonify
from flask.templating import render_template
from sqlalchemy import func

from server.models import User, Comment, Vote, db, State
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

        band_amount = int(Band.query.filter(Band.state == State.IN_VOTE).count())
        print band_amount

        users = User.query.all()
        dict = {'user_count': 0, 'user_voted': 0, 'user_voted_2digit': 0, 'user_voted_all': 0}

        for user in users:
            dict['user_count'] += 1
            if user.vote_count > 0:
                dict['user_voted'] += 1
            if user.vote_count > 9:
                dict['user_voted_2digit'] += 1
            if user.vote_count >= band_amount:
                dict['user_voted_all'] += 1

        dict['vote_count'] = Vote.query.count()
        dict['vote_average'] = round(float(dict['vote_count']) / dict['user_voted'], 2)
        dict['vote_average2'] = round(float(dict['vote_count']) / dict['user_voted_2digit'], 2)
        dict['votes_min'] = db.session.query(func.count(Vote.band_id).label('count')).group_by(Vote.band_id).order_by('count').limit(1).all()[0][0]
        dict['votes_max'] = db.session.query(func.count(Vote.band_id).label('count')).group_by(Vote.band_id).order_by('count DESC').limit(1).all()[0][0]

        dict['votes_avg_min'] = db.session.query(func.avg(Vote.vote).label('avg')).group_by(Vote.band_id).order_by('avg').limit(1).all()[0][0]
        dict['votes_avg_max'] = db.session.query(func.avg(Vote.vote).label('avg')).group_by(Vote.band_id).order_by('avg DESC').limit(1).all()[0][0]
        dict['votes_avg'] = db.session.query(func.avg(Vote.vote)).limit(1).all()[0][0]

        return render_template('statistics.html', dict=dict)


class VoteStatisticsJSON(RestrictedUserPage):
    def get(self):
        vote_query = db.session.query(func.day(Vote.timestamp), func.count(Vote.user_id)).filter(
            func.day(Vote.timestamp) > 1).group_by(Vote.user_id, func.day(Vote.timestamp))
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
        users = User.query.order_by(func.random()).all()
        return render_template('users_overview.html', users=users)