# coding=utf-8
from os import unlink
from uuid import uuid4

from flask import Blueprint, request, jsonify
from flask.templating import render_template
from server.app import trackPool
from server.bands import RestrictedBandPage, AjaxForm, AjaxException
from server.bands.forms import TrackUploadForm

from server.models import db, Track

class TrackUpload(RestrictedBandPage, AjaxForm):
    def __init__(self):
        super(RestrictedBandPage, self).__init__()
        super(AjaxForm, self).__init__()
        self.form = TrackUploadForm()

    def on_submit(self):
        if self.band.tracks.count() == 5:
            raise AjaxException(u'Es dürfen nur maximal 5 Demo-Songs hochgeladen werden.')
        else:
            track = Track()
            track.band_id = self.band.id
            trackFilename = str(self.band.id) + '_' + str(uuid4()) + '.mp3'
            track.filename = trackPool.save(request.files[self.form.audioFile.name], name=trackFilename)
            track.trackname = self.form.trackname.data
            db.session.add(track)
            db.session.commit()
            return {'track': render_template("track_item.html", track=track),
                    'check_tab': render_template('check.html')}


class TrackDelete(RestrictedBandPage):
    def post(self, track_id):
        track = Track.query.get_or_404(track_id)
        unlink(track.path)
        db.session.delete(track)
        db.session.commit()
        return jsonify({'check_tab': render_template('check.html')})


tracks = Blueprint('bands.tracks', __name__, template_folder='../../client/views/bands')
tracks.add_url_rule('/tracks', view_func=TrackUpload.as_view('upload'))
tracks.add_url_rule('/tracks/delete/<int:track_id>', view_func=TrackDelete.as_view('delete'))