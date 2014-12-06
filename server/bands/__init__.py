from flask import session, redirect, url_for, g, jsonify
from flask.views import MethodView
from server.models import Band


class RestrictedBandPage(MethodView):
    def dispatch_request(self, *args, **kwargs):
        if not 'bandId' in session:
            return redirect(url_for('bands.session.index'))
        else:
            self.band = Band.query.get(session['bandId'])
            if not self.band:
                return redirect(url_for('bands.session.index'))
            else:
                g.band = self.band
                return super(RestrictedBandPage, self).dispatch_request(*args, **kwargs)


class AjaxException(Exception):
    errors = []

    def __init__(self, *args):
        super(Exception, self).__init__()
        self.errors = args


AJAX_SUCCESS = []


class AjaxForm(MethodView):
    def post(self):
        if self.form.validate_on_submit():
            try:
                return jsonify(self.on_submit())
            except AjaxException as e:
                errors = self.form.errors
                if len(e.errors) > 0:
                    errors['general'] = e.errors
                return jsonify(errors=errors), 400
        else:
            return jsonify(errors=self.form.errors), 400
