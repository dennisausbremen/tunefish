from flask import jsonify, request
from flask.ext.images import resized_img_src
from server.models import Band, State, db, Vote, Comment
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
            "tracks": [{
                           "trackname": track.trackname,
                           "url": track.url,
                       } for track in band.tracks],
            "comments": [{
                             "author": comment.author.login,
                             "timestamp": comment.timestamp,
                             "message": comment.message,
                         } for comment in band.comments]
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


class JsonCommentAdd(RestrictedUserPage):
    def post(self):
        band_id = int(request.form["band_id"])
        comment_text = str(request.form["comment"])
        band = Band.query.get_or_404(band_id)
        if band and 0 < len(comment_text) < 1001:
            comment = Comment()
            comment.author_id = self.user.id
            comment.message = comment_text.strip()
            comment.band_id = band_id
            db.session.add(comment)
            db.session.commit()

            return jsonify({
                             "author": comment.author.login,
                             "timestamp": comment.timestamp,
                             "message": comment.message,
                         })
        else:
            return jsonify({
                "error": "Der Kommentar darf nur zwischen 1 und 1000 Zeichen lang sein."
            })





