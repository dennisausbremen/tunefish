# coding=utf-8
from os import unlink
from uuid import uuid4

from flask import Blueprint, session, redirect, url_for, request
from flask.templating import render_template
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from server.app import trackPool
from server.bands.forms import AudioForm

from server.models import db, Track


tracks = Blueprint('bands.tracks', __name__, template_folder='../../client/views/bands')


class Audio(MethodView):
    def render(self, audioForm):
        tracks = Track.query.filter_by(band_id=session['bandId'])
        return render_template('audio.html', audioForm=audioForm, tracks=tracks, trackPool=trackPool)


    def get(self):
        return self.render(AudioForm())


class AudioGeneral(Audio):
    def post(self):
        audioForm = AudioForm()
        if audioForm.validate_on_submit():
            try:
                track = Track()
                track.band_id = session['bandId']
                trackFilename = str(session['bandId']) + '_' + str(uuid4()) + '.mp3'
                track.filename = trackPool.save(request.files[audioForm.audioFile.name], name=trackFilename)
                track.trackname = audioForm.trackname.data
                db.session.add(track)
                db.session.commit()
                return self.render(audioForm)
            except IntegrityError as e:
                audioForm.trackname.errors.append("Fehler")
                return self.render(audioForm)
        return self.render(audioForm)


class AudioDelete(Audio):
    def get(self, track_id):
        track = Track.query.get_or_404(track_id)
        filename = trackPool.path(track.filename)
        unlink(filename)
        db.session.delete(track)
        db.session.commit()
        return redirect(url_for('bands.tracks.audio'))


tracks.add_url_rule('/audio', view_func=Audio.as_view('audio'))
tracks.add_url_rule('/audioGeneral', view_func=AudioGeneral.as_view('audioGeneral'))
tracks.add_url_rule('/audioDelete/<int:track_id>', view_func=AudioDelete.as_view('audioDelete'))