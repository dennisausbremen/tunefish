from flask import session, redirect, url_for, g
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