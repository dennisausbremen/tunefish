# coding=utf-8
import mimetypes
from os import unlink
from uuid import uuid4

from flask import Blueprint, request
from server.app import imagePool
from server.bands import RestrictedBandPage, AjaxForm, AJAX_SUCCESS
from server.bands.forms import ImageUploadForm


class ImageUpload(RestrictedBandPage, AjaxForm):
    def __init__(self):
        super(RestrictedBandPage, self).__init__()
        super(AjaxForm, self).__init__()
        self.form = ImageUploadForm()

    def on_submit(self):
        oldfile = None
        if self.band.image:
            oldfile = self.band.image_path
        mimetype = request.files[self.form.image_file.name].mimetype
        ext = mimetypes.guess_extension(mimetype)
        filename = str(self.band.id) + '_' + str(uuid4()) + ext
        self.band.image = imagePool.save(request.files[self.form.image_file.name], name=filename)
        if oldfile:
            unlink(oldfile)
        return AJAX_SUCCESS


images = Blueprint('bands.images', __name__, template_folder='../../client/views/bands')
images.add_url_rule('/images', view_func=ImageUpload.as_view('upload'))