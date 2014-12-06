# coding=utf-8
from os import unlink
from uuid import uuid4

from flask import Blueprint, request, render_template

from server.app import techriderPool
from server.bands import RestrictedBandPage, AjaxForm
from server.bands.forms import TechriderUploadForm
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
        techriderFilename = str(self.band.id) + '_' + str(uuid4()) + '.pdf'
        self.band.techrider = techriderPool.save(request.files[self.form.techriderFile.name], name=techriderFilename)
        db.session.commit()
        if oldTechrider:
            try:
                unlink(oldTechrider)
            except:
                pass
        return {"techrider": render_template('techrider_link.html'),
                'check_tab': render_template('check.html')}


techrider = Blueprint('bands.techrider', __name__, template_folder='../../client/views/bands')
techrider.add_url_rule('/techrider', view_func=TechriderUpload.as_view('upload'))