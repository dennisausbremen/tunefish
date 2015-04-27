import mimetypes
import os
import re
from urllib import quote_plus
import urllib2
from math import ceil
from datetime import datetime

from flask import jsonify, request, g, json, send_file, Response
from sqlalchemy import func

from server import app
from server.models import Band, State, db, Vote, Comment, Track
from server.vote.session_mgmt import RestrictedUserPage


def band2json(band):
    return {
        "id": band.id,
        "name": band.name,
        "members": band.amount_members,
        "city": band.city,
        "website": band.website,
        "descp": band.nl2br_desc(),
        "facebookUrl": band.facebook_url,
        "youtubeUrl": band.youtube_url,
        "image": band.prev_image,
        "thumbnail": band.thumbnail,
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
        "url": track.get_track_url(),
        "band": track.band_id
    }


class JsonBandList(RestrictedUserPage):
    def get(self):
        # random for sqlite, rand for mysql
        state_list = [State.IN_VOTE, State.REQUESTED, State.ACCEPTED, State.DECLINED]
        bands = Band.query.order_by(func.random()).filter(Band.state.in_(state_list))
        return jsonify(bands=[band2json(band) for band in bands],
                       tracks=[track2json(track) for track in Track.query.join(Band).filter(
                           Band.state.in_(state_list))],
                       comments=[comment2json(comment) for comment in
                                 Comment.query.join(Band).filter(Band.state.in_(state_list))])


class JsonBandDetails(RestrictedUserPage):
    def get(self, band_id):
        band = Band.query.get_or_404(band_id)
        if band.state == State.NEW or band.state == State.OUT_OF_VOTE:
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
        if datetime.strptime(app.SETTINGS['BAND_CANDIDATURE_END'], "%Y-%m-%d %H:%M:%S") < datetime.now():
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
            band = Band.query.get(band_id)  # reload because of new average

        return jsonify(band=band2json(band))


class JsonCommentAdd(RestrictedUserPage):
    def post(self):
        data = json.loads(request.data)
        comment = data["comment"]

        band_id = int(comment["band"])
        comment_text = comment["message"]

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
            distance_api = urllib2.urlopen(
                'http://maps.googleapis.com/maps/api/distancematrix/json?origins=' + city + '&destinations=Bremen,Spittaler%20Stra%C3%9Fe%201&language=de-DE&sensor=false')
            distance_json = distance_api.read()
            distance = json.loads(str(distance_json))

            if distance['status'] == "OK":
                value = float(distance['rows'][0]['elements'][0]['distance']['value'])
                band.distance = int(ceil(value / 1000))
                db.session.add(band)
                db.session.commit()

                return jsonify({'success': True, 'distance': band.distance})
            else:
                return jsonify({'success': False, 'distance': 'failed'})


class TrackStreaming(RestrictedUserPage):
    def get(self, track_id):
        track = Track.query.get_or_404(track_id)
        return send_file_partial(track.path)


# fix problems with google chrome
# gist: https://gist.github.com/lizhiwei/7885684
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response


def send_file_partial(path):
    """
        Simple wrapper around send_file which handles HTTP 206 Partial Content
        (byte ranges)
        TODO: handle all send_file args, mirror send_file's error handling
        (if it has any)
    """
    range_header = request.headers.get('Range', None)
    if not range_header: return send_file(path)

    size = os.path.getsize(path)
    byte1, byte2 = 0, None

    m = re.search('(\d+)-(\d*)', range_header)
    g = m.groups()

    if g[0]: byte1 = int(g[0])
    if g[1]: byte2 = int(g[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1

    data = None
    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data,
                  206,
                  mimetype=mimetypes.guess_type(path)[0],
                  direct_passthrough=True)
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size))

    return rv