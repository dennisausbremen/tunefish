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


class JsonBandDetails(RestrictedUserPage):
    def get(self, band_id):
        band = Band.query.get_or_404(band_id)
        return jsonify({
            "id": band.id,
            "name": band.name,
            "amount_members": band.amount_members,
            "city": band.city,
            "website": band.website,
            "descp": band.descp,
            "image_url": band.image_url,
            "vote_count": band.vote_count,
            "vote_average": band.vote_average,
            "tracks": [],
            "comments": []
        })