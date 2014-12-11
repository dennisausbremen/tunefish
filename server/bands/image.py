# coding=utf-8
from os import unlink
from uuid import uuid4

from flask import request
from flask.ext.uploads import UploadNotAllowed
from flask.templating import render_template
from server.ajax import AjaxException
from server.app import imagePool
from server.bands.forms import ImageUploadForm
from server.bands.session_mgmt import RestrictedBandAjaxForm
from server.models import db


class ImageUpload(RestrictedBandAjaxForm):
    def __init__(self):
        super(RestrictedBandAjaxForm, self).__init__()
        self.form = ImageUploadForm()

    def on_submit(self):
        oldfile = None
        if self.band.image:
            oldfile = self.band.image_path
        filename = str(self.band.id) + '_' + str(uuid4()) + '.'
        try:
            self.band.image = imagePool.save(request.files[self.form.image_file.name], name=filename)
        except UploadNotAllowed:
            raise AjaxException(u'Nur jpg, png, gif erlaubt')
        db.session.commit()
        if oldfile:
            try:
                unlink(oldfile)
            except:
                pass
        return {"image": render_template('image_preview.html'),
                'check_tab': render_template('check.html')}
