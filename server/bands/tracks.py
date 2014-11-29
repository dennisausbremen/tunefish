# coding=utf-8
from os import unlink
from uuid import uuid4

from flask import Blueprint, redirect, url_for, request
from flask.templating import render_template
from server.app import trackPool
from server.bands import RestrictedBandPage
from server.bands.forms import TrackUploadForm

from server.models import db, Track


class TrackPage(RestrictedBandPage):
    def __init__(self):
        super(RestrictedBandPage, self).__init__()
        self.uploadForm = TrackUploadForm()

    def render(self):
        tracks = self.band.tracks.all()
        return render_template('tracks.html', uploadForm=self.uploadForm, tracks=tracks)

    def get(self):
        return self.render()


class TrackUpload(TrackPage):
    def post(self):
        audioForm = TrackUploadForm()
        if audioForm.validate_on_submit():
            track = Track()
            track.band_id = self.band.id
            trackFilename = str(self.band.id) + '_' + str(uuid4()) + '.mp3'
            track.filename = trackPool.save(request.files[audioForm.audioFile.name], name=trackFilename)
            track.trackname = audioForm.trackname.data
            db.session.add(track)
            db.session.commit()

        return self.render()


class TrackDelete(RestrictedBandPage):
    def get(self, track_id):
        track = Track.query.get_or_404(track_id)
        filename = trackPool.path(track.filename)
        unlink(filename)
        db.session.delete(track)
        db.session.commit()
        return redirect(url_for('bands.tracks.index'))


tracks = Blueprint('bands.tracks', __name__, template_folder='../../client/views/bands')
tracks.add_url_rule('/tracks', view_func=TrackPage.as_view('index'))
tracks.add_url_rule('/tracks', view_func=TrackUpload.as_view('upload'))
tracks.add_url_rule('/tracks/delete/<int:track_id>', view_func=TrackDelete.as_view('delete'))