# coding=utf-8
from os import unlink
from flask import flash, url_for, redirect, jsonify
from flask.templating import render_template
from server.bands.mails import send_reminder_mail, send_decline_mail, send_remind_start_mail, send_registration_mail
from server.models import Band, State, db, Comment, Reminder
from server.vote.session_mgmt import RestrictedModAdminPage


class AdminBandView(RestrictedModAdminPage):
    def get(self, band_id):
        band = Band.query.get(band_id)
        if band:
            return render_template('admin/band_view.html', band=band)
        else:
            flash('Es existiert keine Band mit dieser ID', 'error')
            return redirect(url_for('vote.admin.index'))


class AdminRemindBands(RestrictedModAdminPage):
    def get(self):
        bands = Band.query.filter(Band.state == State.NEW)
        for band in bands:
            send_reminder_mail(band)

        return render_template('admin/band_mail.html', bands=bands, type='Erinnerung')


class AdminDeclineBands(RestrictedModAdminPage):
    def get(self):
        bands = Band.query.filter(Band.state == State.IN_VOTE)
        for band in bands:
            send_decline_mail(band)

        return render_template('admin/band_mail.html', bands=bands, type='Absage')


class AdminInformBandsAboutVoting(RestrictedModAdminPage):
    def get(self):
        reminder = Reminder.query.all()
        for remind in reminder:
            send_remind_start_mail(remind)

        return render_template('admin/old_bands_reminder_mail.html', reminders=reminder)


class AdminBandVoteState(RestrictedModAdminPage):
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


class AdminResendActivationMail(RestrictedModAdminPage):
    def get(self, band_id):
        band = Band.query.get(band_id)
        if band:
            if band.state == State.NEW:
                send_registration_mail(band)
                flash('Der Band "' + band.name + '" wurde erneut eine Aktivierungsmail zugeschickt.', 'success')
            else:
                flash('Diese Bandbewerbung ist bereits abgeschlossen.', 'error')
        else:
            flash('Es existiert keine Band mit dieser ID', 'error')
        return redirect(url_for('vote.admin.index'))


class AdminBandState(RestrictedModAdminPage):
    def get(self, band_id, state):
        if state == State.DECLINED or state == State.ACCEPTED or state == State.REQUESTED:
            band = Band.query.get(band_id)
            if band:
                band.state = state
                db.session.commit()
                return jsonify({'success': True, 'state': band.state_label, 'message': 'Band %s %s (ohne E-Mailbenachrichtigung)' % (band.name, band.state_label.lower())})
            return jsonify({'success': False, 'active': False, 'message': u'Es existiert keine Band mit dieser ID'})
        return jsonify({'success': False, 'active': False, 'message': u'Diesen Zustand darf die Band nicht annehmen.'})



class AdminBandDelete(RestrictedModAdminPage):
    def get(self, band_id):
        band = Band.query.get(band_id)
        if band:
            if band.state == State.NEW:
                # delete all the files that may exist for the band
                try:
                    unlink(band.image_path)
                except Exception:
                    pass
                try:
                    unlink(band.techrider_path)
                except Exception:
                    pass
                for track in band.tracks:
                    try:
                        unlink(track.path)
                    except Exception:
                        pass

                # delete the band itself
                db.session.delete(band)
                db.session.commit()

                flash(u'Band "%s" gelöscht' % band.name)
                return redirect(url_for('vote.admin.index'))
            else:
                flash(u'Bands mit abgeschlossener Bewerbung können nicht gelöscht werden.')
                return redirect(url_for('vote.admin.index'))
        else:
            flash(u'Es existiert keine Band mit dieser ID.')
            return redirect(url_for('vote.admin.index'))



class AdminCommentRemove(RestrictedModAdminPage):
    def get(self, comment_id):
        comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return jsonify({'success': True, 'message': u'Kommentar von "%s" gelöscht.' % comment.author.login})
        return jsonify({'success': False, 'message': 'Kommentar nicht gefunden.'})
