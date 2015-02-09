# coding=utf-8
from flask import flash, url_for, redirect, jsonify
from flask.templating import render_template

from server.models import Band, State, db, Comment
from server.vote.session_mgmt import RestrictedModAdminPage


class AdminBandView(RestrictedModAdminPage):
    def get(self, band_id):
        band = Band.query.get(band_id)
        if band:
            return render_template('admin/band_view.html', band=band)
        else:
            flash('Es existiert keine Band mit dieser ID', 'error')
            return redirect(url_for('vote.admin.index'))


class AdminBandState(RestrictedModAdminPage):
    def get(self, band_id):
        band = Band.query.get(band_id)
        if band:
            if band.state == State.IN_VOTE:
                band.state = State.OUT_OF_VOTE
                db.session.commit()
                return jsonify({'success': True, 'state': False, 'message': 'Band %s aus dem Voting genommen' % band.name})
            else:
                band.state = State.IN_VOTE
                db.session.commit()
                return jsonify({'success': True, 'state': True, 'message': 'Band %s wieder in das Voting aufgenommen' % band.name})

        else:
            return jsonify({'success': False, 'active': False, 'message': u'Es existiert keine Band mit dieser ID'})


class AdminCommentRemove(RestrictedModAdminPage):
    def get(self, comment_id):
        comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return jsonify({'success': True, 'message': u'Kommentar von "%s" gelöscht.' % comment.author.login})
        return jsonify({'success': False, 'message': 'Kommentar nicht gefunden.'})
