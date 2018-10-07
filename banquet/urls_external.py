from django.conf.urls import url
from banquet.views import (
    ExternalInviteRedirectView,
    ExternalInviteCreateView,
    ExternalInviteUpdateView,
    ThankYouView,
)

urlpatterns = [
	#external invite
	url(r'^invitation/(?P<token>[0-9A-Fa-f-]+)$', ExternalInviteRedirectView.as_view(), name = 'external_invite_redirect'),
	url(r'^invitation/(?P<token>[0-9A-Fa-f-]+)/create$', ExternalInviteCreateView.as_view(), name = 'external_invite_create'),
	url(r'^invitation/(?P<token>[0-9A-Fa-f-]+)/update$', ExternalInviteUpdateView.as_view(), name = 'external_invite_update'),
	url(r'^invitation/(?P<token>[0-9A-Fa-f-]+)/thank_you$', ThankYouView.as_view(), name = 'external_invite_thankyou'),
]
