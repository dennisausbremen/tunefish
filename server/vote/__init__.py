# coding=utf-8

from flask import Blueprint
from server.vote.ajax import JsonBandList, JsonBandDetails, JsonBandVote, JsonCommentAdd, JsonDistance
from server.vote.band_mgmt import AdminBandView, AdminBandState, AdminCommentRemove
from server.vote.band_vote import BandApp

from server.vote.profile import InactiveUserIndex, AdminIndex
from server.vote.session_mgmt import LoginAndRegisterUser, LogoutUser, RegisterUser, LoginUser
from server.vote.user_mgmt import AdminUserActivation, AdminUserAccess


vote_blueprint = Blueprint('vote', __name__, template_folder='../../client/views/vote')

vote_blueprint.add_url_rule('/', view_func=LoginAndRegisterUser.as_view('session.index'), methods=['GET'])
vote_blueprint.add_url_rule('/', view_func=LoginUser.as_view('session.login'), methods=['POST'])
vote_blueprint.add_url_rule('/register', view_func=RegisterUser.as_view('session.register'))
vote_blueprint.add_url_rule('/logout', view_func=LogoutUser.as_view('session.logout'))

vote_blueprint.add_url_rule('/inactive', view_func=InactiveUserIndex.as_view('home.inactive'))

vote_blueprint.add_url_rule('/admin', view_func=AdminIndex.as_view('admin.index'))
vote_blueprint.add_url_rule('/admin/bands/<int:band_id>', view_func=AdminBandView.as_view('admin.bands.view'))
vote_blueprint.add_url_rule('/admin/bands/<int:band_id>/vote_state', view_func=AdminBandState.as_view('admin.bands.vote_state'))

vote_blueprint.add_url_rule('/admin/users/<int:user_id>/activate', view_func=AdminUserActivation.as_view('admin.users.access'))
vote_blueprint.add_url_rule('/admin/users/<int:user_id>/access_mod', view_func=AdminUserAccess.as_view('admin.users.access_mod'))

vote_blueprint.add_url_rule('/admin/comments/<int:comment_id>/remove', view_func=AdminCommentRemove.as_view('admin.comments.remove'))




vote_blueprint.add_url_rule('/app', view_func=BandApp.as_view('bands.app'))

### ajax
vote_blueprint.add_url_rule('/ajax/bands', view_func=JsonBandList.as_view('ajax.bands'))
vote_blueprint.add_url_rule('/ajax/bands/<int:band_id>', view_func=JsonBandDetails.as_view('ajax.bands.details'), methods=['GET'])
vote_blueprint.add_url_rule('/ajax/bands/<int:band_id>', view_func=JsonBandVote.as_view('ajax.bands.vote'), methods=['PUT'])
vote_blueprint.add_url_rule('/ajax/comments', view_func=JsonCommentAdd.as_view('ajax.comment.add'))
vote_blueprint.add_url_rule('/ajax/distance/<int:band_id>', view_func=JsonDistance.as_view('ajax.distance'))