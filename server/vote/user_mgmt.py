# coding=utf-8
from flask import jsonify, render_template
from server.bands.mails import send_activation_mail, send_user_reminder_mail
from server.models import Access, User, db
from server.vote.session_mgmt import RestrictedAdminPage, RestrictedModAdminPage


class AdminUserActivation(RestrictedModAdminPage):
    def get(self, user_id):
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'active': False, 'message': 'Kein Benutzer mit dieser ID'})
        else:
            if user.is_inactive:
                user.access = Access.USER
                db.session.commit()
                send_activation_mail(user)
                return jsonify({'success': True, 'active': True, 'message': u'Benutzer %s ist jetzt aktiviert' % user.login})
            elif user.is_user:
                user.access = Access.INACTIVE
                db.session.commit()
                return jsonify({'success': True, 'active': False, 'message': u'Benutzer %s ist jetzt deaktiviert' % user.login})
            else:
                return jsonify({'success': False, 'active': True, 'message': u'Du kannst keine Berechtigungen von Moderatoren/Admins ändern'})


class AdminSentUserReminder(RestrictedAdminPage):
    def get(self):
        users = User.query.get(1)#()
        send_user_reminder_mail(users)
        return '', 200

        for user in users:
            if user.vote_count < 135:
                print user.login
                send_user_reminder_mail(user)
        return render_template('admin/user_notify.html', users=users)


class AdminUserAccess(RestrictedAdminPage):
    def get(self, user_id):
        user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'mod': False, 'message': 'Kein Benutzer mit dieser ID'})
        else:
            if user.is_mod:
                user.access = Access.USER
                db.session.commit()
                return jsonify({'success': True, 'mod': False, 'message': u'Benutzer %s hat jetzt Zugriff "Benutzer"' % user.login})
            elif user.is_user:
                user.access = Access.MODERATOR
                db.session.commit()
                return jsonify({'success': True, 'mod': True, 'message': u'Benutzer %s hat jetzt Zugriff "Moderator"' % user.login})
            else:
                return jsonify({'success': False, 'active': False, 'message': u'Du kannst keine Berechtigungen ändern'})


