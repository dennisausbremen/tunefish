# coding=utf-8

from flask import Blueprint

from server.vote.ajax import JsonBandList, JsonBandDetails, JsonBandVote, JsonCommentAdd, JsonDistance, TrackStreaming, \
    after_request
from server.vote.ajaxV2 import BandListJsonV2, BandJsonV2, TrackV2, BandVoteV2, BandCommentV2
from server.vote.band_mgmt import AdminBandView, AdminBandState, AdminCommentRemove, AdminRemindBands, AdminBandDelete, \
    AdminBandVoteState, AdminDeclineBands, AdminInformBandsAboutVoting, AdminResendActivationMail
from server.vote.band_vote import BandApp
from server.vote.profile import InactiveUserIndex, AdminIndex, VotingOverview, VoteStatisticsJSON, VoteStatistics, \
    VoteResults
from server.vote.session_mgmt import LoginAndRegisterUser, LogoutUser, RegisterUser, LoginUser
from server.vote.user_mgmt import AdminUserActivation, AdminUserAccess


vote_blueprint = Blueprint('vote', __name__, template_folder='../../client/views/vote')

vote_blueprint.add_url_rule('/', view_func=LoginAndRegisterUser.as_view('session.index'), methods=['GET'])
vote_blueprint.add_url_rule('/', view_func=LoginUser.as_view('session.login'), methods=['POST'])
vote_blueprint.add_url_rule('/register', view_func=RegisterUser.as_view('session.register'))
vote_blueprint.add_url_rule('/logout', view_func=LogoutUser.as_view('session.logout'))

vote_blueprint.add_url_rule('/inactive', view_func=InactiveUserIndex.as_view('home.inactive'))

vote_blueprint.add_url_rule('/results', view_func=VoteResults.as_view('home.vote_results'))

vote_blueprint.add_url_rule('/admin', view_func=AdminIndex.as_view('admin.index'))
vote_blueprint.add_url_rule('/admin/bands/<int:band_id>', view_func=AdminBandView.as_view('admin.bands.view'))
vote_blueprint.add_url_rule('/admin/bands/<int:band_id>/vote_state',
                            view_func=AdminBandVoteState.as_view('admin.bands.vote_state'))
vote_blueprint.add_url_rule('/admin/bands/<int:band_id>/<int:state>',
                            view_func=AdminBandState.as_view('admin.bands.band_state'))
vote_blueprint.add_url_rule('/admin/bands/<int:band_id>/delete',
                            view_func=AdminBandDelete.as_view('admin.bands.delete'))
vote_blueprint.add_url_rule('/admin/bands/<int:band_id>/resendConfirmation',
                            view_func=AdminResendActivationMail.as_view('admin.bands.resendConfirmation'))

vote_blueprint.add_url_rule('/admin/users/<int:user_id>/activate',
                            view_func=AdminUserActivation.as_view('admin.users.access'))
vote_blueprint.add_url_rule('/admin/users/<int:user_id>/access_mod',
                            view_func=AdminUserAccess.as_view('admin.users.access_mod'))

vote_blueprint.add_url_rule('/admin/comments/<int:comment_id>/remove',
                            view_func=AdminCommentRemove.as_view('admin.comments.remove'))

# vote_blueprint.add_url_rule('/admin/reminder', view_func=AdminRemindBands.as_view('admin.remind'))
# vote_blueprint.add_url_rule('/admin/decline', view_func=AdminDeclineBands.as_view('admin.decline'))
# vote_blueprint.add_url_rule('/admin/inform_bands', view_func=AdminInformBandsAboutVoting.as_view('admin.inform'))



vote_blueprint.add_url_rule('/app', view_func=BandApp.as_view('bands.app'))

vote_blueprint.add_url_rule('/progress', view_func=VotingOverview.as_view('voting.overview'))
vote_blueprint.add_url_rule('/stats', view_func=VoteStatistics.as_view('stats.vote'))
vote_blueprint.add_url_rule('/stats/json', view_func=VoteStatisticsJSON.as_view('stats.vote_json'))


### ajax
vote_blueprint.add_url_rule('/ajax/bands', view_func=JsonBandList.as_view('ajax.bands'))
vote_blueprint.add_url_rule('/ajax/bands/<int:band_id>', view_func=JsonBandDetails.as_view('ajax.bands.details'),
                            methods=['GET'])
vote_blueprint.add_url_rule('/ajax/bands/<int:band_id>', view_func=JsonBandVote.as_view('ajax.bands.vote'),
                            methods=['PUT'])
vote_blueprint.add_url_rule('/ajax/comments', view_func=JsonCommentAdd.as_view('ajax.comment.add'))
vote_blueprint.add_url_rule('/ajax/distance/<int:band_id>', view_func=JsonDistance.as_view('ajax.distance'))

vote_blueprint.add_url_rule('/api/v2/bands', view_func=BandListJsonV2.as_view('api.v2.bands'))
vote_blueprint.add_url_rule('/api/v2/bands/<int:band_id>', view_func=BandJsonV2.as_view('api.v2.band'))
vote_blueprint.add_url_rule('/api/v2/bands/<int:band_id>/vote', view_func=BandVoteV2.as_view('api.v2.vote'),methods=['PUT'])
vote_blueprint.add_url_rule('/api/v2/bands/<int:band_id>/comment', view_func=BandCommentV2.as_view('api.v2.comment'))


# own blueprint, because of the after request
track_blueprint = Blueprint('track', __name__, template_folder='../../client/views/vote')
track_blueprint.add_url_rule('/ajax/track/<int:track_id>.mp3', view_func=TrackStreaming.as_view('ajax.track'))
track_blueprint.add_url_rule('/api/v2/track/<int:track_id>.mp3', view_func=TrackV2.as_view('api.v2.track'))
track_blueprint.after_request(after_request)
