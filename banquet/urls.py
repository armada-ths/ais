from django.conf.urls import url
from banquet.views import (
    InternalInviteView,
    ExternalInviteView,
    SentInvitationsListView,
    ParticipantsListView,
    SendInviteCreateView,
    ThankYouView,
    export_invitations
)

from django.conf import settings
from django.conf.urls.static import  static


urlpatterns = [
	url(r'^internal_invite/$', InternalInviteView.as_view(), name = 'internal_invite'),
	url(r'^(?P<token>[0-9A-Fa-f-]+)/invite/$', ExternalInviteView.as_view(), name = 'external_invite'),
	url(r'^$', SentInvitationsListView.as_view(), name = 'invite_list'),
	url(r'^participants/$', ParticipantsListView.as_view(), name = 'participant_list'),
	url(r'^send/$', SendInviteCreateView.as_view(), name = 'send_invite'),
	url(r'^(?P<token>[0-9A-Fa-f-]+)/thank_you/$', ThankYouView.as_view(), name = 'banquet_thank_you'),
        url(r'^export/$', export_invitations, name='export_invitations')
]
