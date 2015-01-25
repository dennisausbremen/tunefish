# coding=utf-8

from flask import Blueprint
from server.vote.ajax import JsonBandList, JsonBandDetails, JsonBandVote, JsonCommentAdd
from server.vote.band_mgmt import AdminBandList, AdminBandView, AdminBandState
from server.vote.band_vote import BandList, BandDetails, BandCommendAdd, BandVote, BandApp

from server.vote.profile import UserIndex, AdminIndex
from server.vote.session_mgmt import LoginAndRegisterUser, LogoutUser, RegisterUser, LoginUser
from server.vote.user_mgmt import AdminUserList, AdminUserActivation, AdminUserAccess


vote_blueprint = Blueprint('vote', __name__, template_folder='../../client/views/vote')

vote_blueprint.add_url_rule('/', view_func=LoginAndRegisterUser.as_view('session.index'), methods=['GET'])
vote_blueprint.add_url_rule('/', view_func=LoginUser.as_view('session.login'), methods=['POST'])
vote_blueprint.add_url_rule('/register', view_func=RegisterUser.as_view('session.register'))
vote_blueprint.add_url_rule('/logout', view_func=LogoutUser.as_view('session.logout'))

vote_blueprint.add_url_rule('/home', view_func=UserIndex.as_view('home.index'))

vote_blueprint.add_url_rule('/admin', view_func=AdminIndex.as_view('admin.index'))
vote_blueprint.add_url_rule('/admin/bands', view_func=AdminBandList.as_view('admin.bands.list'))
vote_blueprint.add_url_rule('/admin/bands/<int:band_id>', view_func=AdminBandView.as_view('admin.bands.view'))
vote_blueprint.add_url_rule('/admin/bands/<int:band_id>/vote_state', view_func=AdminBandState.as_view('admin.bands.vote_state'))

vote_blueprint.add_url_rule('/admin/users', view_func=AdminUserList.as_view('admin.users.list'))
vote_blueprint.add_url_rule('/admin/users/access/<int:user_id>', view_func=AdminUserActivation.as_view('admin.users.access'))
vote_blueprint.add_url_rule('/admin/users/access_mod/<int:user_id>', view_func=AdminUserAccess.as_view('admin.users.access_mod'))



vote_blueprint.add_url_rule('/app', view_func=BandApp.as_view('bands.app'))
vote_blueprint.add_url_rule('/bands', view_func=BandList.as_view('bands.list'))
vote_blueprint.add_url_rule('/bands/<int:band_id>', view_func=BandDetails.as_view('bands.view'))
vote_blueprint.add_url_rule('/bands/<int:band_id>/vote/<int:vote>', view_func=BandVote.as_view('bands.vote'))

vote_blueprint.add_url_rule('/comment/add', view_func=BandCommendAdd.as_view('comment.add'))


### ajax
vote_blueprint.add_url_rule('/ajax/bands', view_func=JsonBandList.as_view('ajax.bands'))
vote_blueprint.add_url_rule('/ajax/bands/<int:band_id>', view_func=JsonBandDetails.as_view('ajax.bands.details'))
vote_blueprint.add_url_rule('/ajax/bands/vote', view_func=JsonBandVote.as_view('ajax.bands.vote'))
vote_blueprint.add_url_rule('/ajax/comments/add', view_func=JsonCommentAdd.as_view('ajax.comment.add'))
