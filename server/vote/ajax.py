from datetime import datetime
from urllib import quote_plus
import urllib2
from flask import jsonify, request, g, json
from math import ceil
from server.models import Band, State, db, Vote, Comment, Track
from server.vote.session_mgmt import RestrictedUserPage


def band2json(band):
    return {
        "id": band.id,
        "name": band.name,
        "members": band.amount_members,
        "city": band.city,
        "website": band.website,
        "descp": band.descp,
        "facebookUrl": band.facebook_url,
        "youtubeUrl": band.youtube_url,
        "image": band.prev_image,
        "thumbnail": band.thumbnail,
        "voteCount": band.vote_count,
        "voteAverage": band.vote_average,
        "ownVote": band.get_user_vote(g.user),
        "distance": band.distance,
        "comments": [comment.id for comment in band.comments],
        'voted': band.get_user_vote(g.user) > 0
    }


def comment2json(comment):
    return {
        "id": comment.id,
        "author": comment.author.login,
        "timestamp": comment.date_time,
        "message": comment.message,
        "band": comment.band_id
    }

def track2json(track):

    return {
        "id": track.id,
        "trackname": track.nice_trackname,
        "url": track.url,
        "band": track.band_id
    }


class JsonBandList(RestrictedUserPage):
    def get(self):
        bands = Band.query.filter(Band.state == State.IN_VOTE)
        return jsonify(bands=[band2json(band) for band in bands],
                       tracks=[track2json(track) for track in Track.query.join(Band).filter(
                           Band.state == State.IN_VOTE)],
                       comments=[comment2json(comment) for comment in Comment.query.join(Band).filter(
                           Band.state == State.IN_VOTE)])


class JsonBandDetails(RestrictedUserPage):
    def get(self, band_id):
        band = Band.query.get_or_404(band_id)
        if band.state != State.IN_VOTE:
            return '', 404
        else:
            return jsonify(band=band2json(band),
                           comments=[comment2json(comment) for comment in band.comments],
                           tracks=[track2json(track) for track in band.tracks]
        )


class JsonBandVote(RestrictedUserPage):
    def put(self, band_id):
        data = json.loads(request.data)
        vote = int(data["band"]["ownVote"])
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
            band = Band.query.get(band_id) # reload because of new average

        return jsonify(band=band2json(band))


class JsonCommentAdd(RestrictedUserPage):
    def post(self):
        data = json.loads(request.data)
        comment = data["comment"]

        band_id = int(comment["band"])
        comment_text = str(comment["message"])

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


# damn Same-Origin-Rule ...
class JsonDistance(RestrictedUserPage):
    def get(self, band_id):
        band = Band.query.get_or_404(band_id)
        if band:
            city = quote_plus(band.city.encode('utf-8'))
            distance_api = urllib2.urlopen('http://maps.googleapis.com/maps/api/distancematrix/json?origins=' + city + '&destinations=Bremen,Spittaler%20Stra%C3%9Fe%201&language=de-DE&sensor=false')
            distance_json = distance_api.read()
            distance = json.loads(str(distance_json))

            if distance['status'] == "OK":
                value = float(distance['rows'][0]['elements'][0]['distance']['value'])
                band.distance = int(ceil(value/1000))
                db.session.add(band)
                db.session.commit()

                return jsonify({'success': True, 'distance': band.distance})
            else:
                return jsonify({'success': False, 'distance': 'failed'})