from datetime import datetime

from flask import jsonify, g, json, request
from flask.ext.jwt import current_identity, jwt_required
from sqlalchemy import func

from server import app
from server.models import Band, State, Track, Vote, db, Comment
from server.vote.ajax import send_file_partial
from server.vote.session_mgmt import LoginAndRegisterUser, RestrictedUserPage


def simpleBand(band):
    return {
        "id": band.id,
        "artist": band.name,
        "image": {"thumb": band.thumbnail},
        "rating": band.get_user_vote(g.user)
    }


def band2json(band):
    return {
        "id": band.id,
        "artist": band.name,
        "image": {"thumb": band.thumbnail, "poster": band.prev_image},
        "description": band.nl2br_desc(),
        "facebookURL": band.facebook_url,
        "websiteURL": band.website,
        "youtubeURL": band.youtube_url,
        "rating": band.get_user_vote(g.user),
        "comments": [comment2json(comment) for comment in band.comments],
        "tracks": [track2json(track, band) for track in band.tracks]
    }


def comment2json(comment):
    return {
        "author": comment.author.login,
        "timestamp": comment.timestamp,
        "message": comment.message,
    }


def track2json(track, band):
    return {
        "id": track.id,
        "artist": band.name,
        "title": track.nice_trackname,
        "url": track.get_track_url_v3(),
    }


class BandListJsonV3(RestrictedUserPage):
    def get(self):
        # random for sqlite, rand for mysql
        state_list = [State.IN_VOTE, State.REQUESTED, State.ACCEPTED, State.DECLINED]

        #bands = Band.query.order_by(func.random()).filter(Band.state.in_(state_list))
        bands = Band.query.filter(Band.state.in_(state_list))
        bands_sorted = sorted(bands, key=lambda x: x.vote_average, reverse=True)

        return jsonify(bands=[simpleBand(band) for band in bands_sorted]), 200, {'Access-Control-Allow-Origin': '*'}


class BandJsonV3(RestrictedUserPage):
    def get(self, band_id):
        band = Band.query.get_or_404(band_id)
        if band.state == State.NEW or band.state == State.OUT_OF_VOTE:
            return '', 404
        else:
            return jsonify(band2json(band)), 200, {'Access-Control-Allow-Origin': '*'}


class TrackV3(RestrictedUserPage):

    def get(self, track_id):
        track = Track.query.get_or_404(track_id)
        return send_file_partial(track.path)


class BandVoteV3(RestrictedUserPage):

    def put(self, band_id):
        data = json.loads(request.data)
        vote = int(data['vote'])
        if datetime.strptime(app.SETTINGS['VOTING_END'], "%Y-%m-%d %H:%M:%S") < datetime.now():
            return '', 404
        band = Band.query.get_or_404(band_id)
        if band and 0 < vote < 6:
            voting = Vote.query.filter(Vote.band_id == band_id, Vote.user_id == self.user.id).first()
            if not voting:
                voting = Vote()
                voting.user_id = self.user.id
                voting.band_id = band_id
                db.session.add(voting)

            voting.vote = vote
            db.session.commit()

        return jsonify()


class BandCommentV3(RestrictedUserPage):

    def post(self, band_id):
        data = json.loads(request.data)
        comment_text = data["comment"]

        band = Band.query.get_or_404(band_id)
        if band and 0 < len(comment_text) < 1001:
            comment = Comment()
            comment.author_id = self.user.id
            comment.message = comment_text.strip()
            comment.band_id = band_id
            db.session.add(comment)
            db.session.commit()

            return jsonify(comment=comment2json(comment))
        else:
            return "{}", 400
