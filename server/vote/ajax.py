from flask import jsonify, request
from flask.ext.images import resized_img_src
from server.models import Band, State, db, Vote
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


class JsonBandVote(RestrictedUserPage):
    def post(self):
        band_id = request.form["band_id"]
        vote = int(request.form["vote"])
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

        return jsonify({
            "vote_count": band.vote_count,
            "vote_average": band.vote_average,
            })

