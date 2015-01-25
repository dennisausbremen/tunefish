# coding=utf-8
from flask import flash, url_for, redirect

from flask.templating import render_template

from server.models import Access, User, db
from server.vote.session_mgmt import RestrictedAdminPage, RestrictedModAdminPage


class AdminUserList(RestrictedModAdminPage):
    def get(self):
        users = User.query.all()
        return render_template('admin/user_list.html', users=users)


class AdminUserActivation(RestrictedModAdminPage):
    def get(self, user_id):
        user = User.query.get(user_id)

        if not user:
            flash('Kein Benutzer mit dieser ID', 'error')
        else:
            if user.is_inactive:
                user.access = Access.USER
                db.session.commit()
                flash(u'Benutzer %s ist jetzt aktiviert' % user.login, 'info')
            elif user.is_user:
                user.access = Access.INACTIVE
                db.session.commit()
                flash(u'Benutzer %s ist jetzt deaktiviert' % user.login, 'info')
            else:
                flash(u'Du kannst keine Berechtigungen von Moderatoren/Admins ändern', 'error')

        return redirect(url_for('vote.admin.users.list'))


class AdminUserAccess(RestrictedAdminPage):
    def get(self, user_id):
        user = User.query.get(user_id)

        if not user:
            flash('Kein Benutzer mit dieser ID', 'error')
        else:
            if user.is_mod:
                user.access = Access.USER
                db.session.commit()
                flash(u'Benutzerzugriff auf "Benutzer" geändert', 'info')
            elif user.is_user:
                user.access = Access.MODERATOR
                db.session.commit()
                flash(u'Benutzerzugriff auf "Moderator" geändert', 'info')
            else:
                flash(u'Du kannst keine Berechtigungen von Benutzern ändern', 'error')

        return redirect(url_for('vote.admin.users.list'))

