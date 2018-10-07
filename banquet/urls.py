from django.conf.urls import url
from banquet.views import (
    InternalInviteRedirectView,
    InternalInviteCreateView,
    InternalInviteUpdateView,
    SentInvitationsListView,
    ParticipantsListView,
    SendInviteCreateView,
    ThankYouView,
    export_invitations
)

from django.conf import settings
from django.conf.urls.static import  static


urlpatterns = [
	#internal invite
	url(r'^internal_invitation$', InternalInviteRedirectView.as_view(), name = 'internal_invite_redirect'),
	url(r'^internal_invitation/create$', InternalInviteCreateView.as_view(), name = 'internal_invite_create'),
	url(r'^internal_invitation/update$', InternalInviteUpdateView.as_view(), name = 'internal_invite_update'),
	url(r'^$', SentInvitationsListView.as_view(), name = 'invite_list'),
	url(r'^participants$', ParticipantsListView.as_view(), name = 'participant_list'),
	url(r'^send$', SendInviteCreateView.as_view(), name = 'send_invite'),
	url(r'^export$', export_invitations, name='export_invitations')
]
