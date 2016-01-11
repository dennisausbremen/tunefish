# coding=utf-8
from datetime import date
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

        return render_template('admin/overview.html', bands=bands, users=users, comments=comments, states=State)


class VoteResults(RestrictedUserPage):
    def get(self):
	return render_template('main_no_results.html')
        state_list = [State.IN_VOTE, State.REQUESTED, State.ACCEPTED, State.DECLINED]
        bands = Band.query.filter(Band.state.in_(state_list))
        return render_template('band_list.html', bands=bands, states=State)


class VoteStatistics(RestrictedUserPage):
    def get(self):

        band_amount = int(Band.query.filter(Band.state == State.IN_VOTE).count())

        users = User.query.all()
        dict = {'user_count': 0, 'user_voted': 0, 'user_voted_1': 0, 'user_voted_2digit': 0, 'user_voted_all': 0}

        for user in users:
            dict['user_count'] += 1
            if user.vote_count > 0:
                dict['user_voted'] += 1
            if user.vote_count == 1:
                dict['user_voted_1'] += 1
            if user.vote_count > 9:
                dict['user_voted_2digit'] += 1
            if user.vote_count >= band_amount:
                dict['user_voted_all'] += 1

        dict['vote_count'] = Vote.query.count()
        dict['vote_average'] = round(float(dict['vote_count']) / dict['user_voted'], 2)
        dict['vote_average2'] = round(float(dict['vote_count']) / dict['user_voted_2digit'], 2)
        start_day = 305 # 3.3. ist der 62. Tag des Jahres
        voting_time = date.today().timetuple().tm_yday - start_day
        dict['votes_per_day'] = round(float(dict['vote_count']) / voting_time, 2)
        base_votes_min_max = db.session.query(func.count(Vote.band_id).label('count')).group_by(Vote.band_id)
        dict['votes_min'] = base_votes_min_max.order_by('count').limit(1).all()[0][0]
        dict['votes_max'] = base_votes_min_max.order_by('count DESC').limit(1).all()[0][0]

        base_votes_avg = db.session.query(func.avg(Vote.vote).label('avg')).group_by(Vote.band_id)
        dict['votes_avg_min'] = round(base_votes_avg.order_by('avg').limit(1).all()[0][0], 2)
        dict['votes_avg_max'] = round(base_votes_avg.order_by('avg DESC').limit(1).all()[0][0], 2)
        dict['votes_avg'] = round(db.session.query(func.avg(Vote.vote)).limit(1).all()[0][0], 2)

        dict['band_amount'] = band_amount
        dict['avg_votes_band'] = round(float(dict['vote_count'])/band_amount, 2)
        dict['comments_count'] = Comment.query.count()
        dict['comments_users'] = Comment.query.group_by(Comment.author_id).count()

        return render_template('statistics.html', dict=dict)


class VoteStatisticsJSON(RestrictedUserPage):
    def get(self):
        vote_query = db.session.query(func.dayofyear(Vote.timestamp), func.count(Vote.user_id)).filter(
            func.dayofyear(Vote.timestamp) > 1).group_by(Vote.user_id, func.dayofyear(Vote.timestamp))
        votes = vote_query.all()

        # initialize the dict with empty data
        day = 305 # 16.3, the starting day; set because previous data has no date!, must be beginning of vote period

        today = date.today().timetuple().tm_yday
        if today < 305:
            today = 365;

        json_vote = {}
        while day <= today:
            json_vote[day] = {'user': 0, 'votes': 0}
            day += 1

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
