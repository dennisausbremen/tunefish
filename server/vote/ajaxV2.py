import mimetypes
import os
import re
from urllib import quote_plus
import urllib2
from math import ceil
from datetime import datetime

from flask import jsonify, request, g, json, send_file, Response, session
from sqlalchemy import func

from server import app
from server.models import Band, State, db, Vote, Comment, Track, User
from server.vote.session_mgmt import RestrictedUserPage, LoginAndRegisterUser


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
        "artist": band.name,
        "title": track.nice_trackname,
        "url": track.get_track_url()
    }


class BandListJsonV2(LoginAndRegisterUser):
    def get(self):
        self.user = User.query.get(3)
        g.user = self.user
        session['userId'] = 3
        # random for sqlite, rand for mysql
        state_list = [State.IN_VOTE, State.REQUESTED, State.ACCEPTED, State.DECLINED]
        bands = Band.query.order_by(func.random()).filter(Band.state.in_(state_list))
        return jsonify([simpleBand(band) for band in bands]), 200, {'Access-Control-Allow-Origin': '*'}


class BandJsonV2(LoginAndRegisterUser):
    def get(self, band_id):
        self.user = User.query.get(3)
        g.user = self.user
        session['userId'] = 3

        band = Band.query.get_or_404(band_id)
        if band.state == State.NEW or band.state == State.OUT_OF_VOTE:
            return '', 404
        else:
            return jsonify(band2json(band)), 200, {'Access-Control-Allow-Origin': '*'}