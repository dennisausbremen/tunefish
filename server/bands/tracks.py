# coding=utf-8

from os import unlink
from uuid import uuid4

from flask import request, jsonify, flash
import flask
from flask.ext.uploads import UploadNotAllowed
from flask.templating import render_template
from server.ajax import AjaxException, AJAX_FAIL
from server.app import trackPool
from server.bands.forms import TrackUploadForm
from server.bands.session_mgmt import RestrictedBandPage, RestrictedBandAjaxForm

from server.models import db, Track, State


class TrackUpload(RestrictedBandAjaxForm):
    def __init__(self):
        super(RestrictedBandAjaxForm, self).__init__()
        self.form = TrackUploadForm()

    def on_submit(self):
        if self.band.tracks.count() == 5:
            raise AjaxException(u'Es dürfen nur maximal 5 Demo-Songs hochgeladen werden.')
        else:
            uploaded_files = flask.request.files.getlist("audioFile[]")
            success = []
            fail = []
            for uploaded_file in uploaded_files:
                if self.band.tracks.count() == 5:
                    fail.append(uploaded_file.filename)
                    continue
                track = Track()
                track.trackname = uploaded_file.filename
                track.band_id = self.band.id
                track_filename = str(self.band.id) + '_' + str(uuid4()) + '.'
                try:
                    track.filename = trackPool.save(uploaded_file, name=track_filename)
                    success.append(uploaded_file.filename)
                except UploadNotAllowed:
                    fail.append(uploaded_file.filename)
                    flash('Fehler beim Upload von Datei ' + uploaded_file.filename)
                db.session.add(track)
                db.session.commit()
            return {'track': render_template("track_item.html"),
                    'check_tab': render_template('check.html'),
                    'fail': fail,
                    'success': success}


class TrackDelete(RestrictedBandPage):
    def post(self, track_id):
        if self.band.state != State.NEW:
            return AJAX_FAIL('Die Banddaten können nach dem Abschluss der Bewerbung nicht mehr geändert werden')
        else:
            track = Track.query.get_or_404(track_id)
            try:
                unlink(track.path)
            except Exception:
                # TODO handle file unlink (use celery task?)
                flash('Fehler beim loeschen')
            db.session.delete(track)
            db.session.commit()
            return jsonify({'check_tab': render_template('check.html')})
