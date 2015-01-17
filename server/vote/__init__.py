# coding=utf-8

from flask import Blueprint
from server.vote.band_mgmt import AdminBandList, AdminBandView

from server.vote.profile import UserIndex, AdminIndex
from server.vote.session_mgmt import LoginAndRegisterUser, LogoutUser, RegisterUser, LoginUser
from server.vote.user_mgmt import AdminUserList, AdminUserAccess


vote_blueprint = Blueprint('vote', __name__, template_folder='../../client/views/vote')

vote_blueprint.add_url_rule('/', view_func=LoginAndRegisterUser.as_view('session.index'), methods=['GET'])
vote_blueprint.add_url_rule('/', view_func=LoginUser.as_view('session.login'), methods=['POST'])
vote_blueprint.add_url_rule('/register', view_func=RegisterUser.as_view('session.register'))
vote_blueprint.add_url_rule('/logout', view_func=LogoutUser.as_view('session.logout'))

vote_blueprint.add_url_rule('/home', view_func=UserIndex.as_view('home.index'))

vote_blueprint.add_url_rule('/admin', view_func=AdminIndex.as_view('admin.index'))
vote_blueprint.add_url_rule('/admin/bands', view_func=AdminBandList.as_view('admin.bands.list'))
vote_blueprint.add_url_rule('/admin/bands/<int:band_id>', view_func=AdminBandView.as_view('admin.bands.view'))

vote_blueprint.add_url_rule('/admin/users', view_func=AdminUserList.as_view('admin.users.list'))
vote_blueprint.add_url_rule('/admin/users/access/<int:user_id>', view_func=AdminUserAccess.as_view('admin.users.access'))


