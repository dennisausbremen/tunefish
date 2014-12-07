# coding=utf-8

from os import unlink
from uuid import uuid4

from flask import request, jsonify
from flask.ext.uploads import UploadNotAllowed
from flask.templating import render_template
from server.ajax import AjaxException, AjaxForm
from server.app import trackPool
from server.bands.forms import TrackUploadForm
from server.bands.session_mgmt import RestrictedBandPage

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
            trackFilename = str(self.band.id) + '_' + str(uuid4()) + '.'
            try:
                track.filename = trackPool.save(request.files[self.form.audioFile.name], name=trackFilename)
            except UploadNotAllowed:
                raise AjaxException(u'Nur mp3s erlaubt')

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
