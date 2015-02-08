# coding=utf-8
from flask import jsonify

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
                return jsonify({'success': True, 'active': True, 'message': u'Benutzer %s ist jetzt aktiviert' % user.login})
            elif user.is_user:
                user.access = Access.INACTIVE
                db.session.commit()
                return jsonify({'success': True, 'active': False, 'message': u'Benutzer %s ist jetzt deaktiviert' % user.login})
            else:
                return jsonify({'success': False, 'active': True, 'message': u'Du kannst keine Berechtigungen von Moderatoren/Admins ändern'})


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


