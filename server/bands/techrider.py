# coding=utf-8

from os import unlink
from uuid import uuid4

from flask import request, render_template
from flask.ext.uploads import UploadNotAllowed
from server.ajax import AjaxException, AjaxForm

from server.app import techriderPool
from server.bands.forms import TechriderUploadForm
from server.bands.session_mgmt import RestrictedBandPage
from server.models import db


class TechriderUpload(RestrictedBandPage, AjaxForm):
    def __init__(self):
        super(RestrictedBandPage, self).__init__()
        super(AjaxForm, self).__init__()
        self.form = TechriderUploadForm()

    def on_submit(self):
        oldTechrider = None
        if self.band.techrider:
            oldTechrider = self.band.techrider_path
        techriderFilename = str(self.band.id) + '_' + str(uuid4()) + '.'
        try:
            self.band.techrider = techriderPool.save(request.files[self.form.techriderFile.name], name=techriderFilename)
        except UploadNotAllowed:
            raise AjaxException(u'Nur pdfs erlaubt')
        db.session.commit()
        if oldTechrider:
            try:
                unlink(oldTechrider)
            except:
                pass
        return {"techrider": render_template('techrider_link.html'),
                'check_tab': render_template('check.html')}
