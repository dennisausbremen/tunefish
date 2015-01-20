from flask import jsonify
from flask.ext.images import resized_img_src
from server.models import Band, State
from server.vote.session_mgmt import RestrictedUserPage


class JsonBandList(RestrictedUserPage):
    def get(self):
        bands = Band.query.filter(Band.state == State.IN_VOTE)
        return jsonify(bands=[{
                                  "id": band.id,
                                  "name": band.name,
                                  "thumbnail": resized_img_src(band.image, mode="crop", width=200, height=200),
                                  "vote_count": band.vote_count,
                                  "vote_average": band.vote_average
                              }
                              for band in bands])
