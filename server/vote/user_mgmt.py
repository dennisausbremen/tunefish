# coding=utf-8
from flask import flash, url_for, redirect

from flask.templating import render_template

from server.models import Access, Band, State, User, db
from server.vote.session_mgmt import RestrictedUserPage


class AdminUserList(RestrictedUserPage):
    def get(self):
        if self.user.is_mod or self.user.is_admin:
            users = User.query.all()
            return render_template('admin/user_list.html', users=users, state=State)
        else:
            flash('Du hast hier keinen Zugriff', 'error')
            return redirect(url_for('vote.home.index'))


class AdminUserAccess(RestrictedUserPage):
    def get(self, user_id):
        if self.user.is_mod or self.user.is_admin:
            user = User.query.get(user_id)

            if not user:
                flash('Kein Benutzer mit dieser ID', 'error')
            else:
                if user.is_inactive:
                    user.access = Access.USER
                    db.session.commit()
                    flash(u'löppt', 'info')
                elif user.is_user:
                    user.access = Access.INACTIVE
                    db.session.commit()

                else:
                    flash(u'Du kannst keine Berechtigungen von Moderatoren/Admins ändern', 'error')

            return redirect(url_for('vote.admin.users.list'))


