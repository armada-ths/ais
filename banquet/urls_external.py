from django.conf.urls import url
from banquet.views import (
    ExternalInviteRedirectView,
    ExternalInviteCreateView,
    ExternalInviteUpdateView,
    ThankYouView,
)

urlpatterns = [
	#external invite
	url(r'^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', ExternalInviteRedirectView.as_view(), name = 'external_invite_redirect'),
	url(r'^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/create$', ExternalInviteCreateView.as_view(), name = 'external_invite_create'),
	url(r'^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/update$', ExternalInviteUpdateView.as_view(), name = 'external_invite_update'),
	url(r'^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/thank_you$', ThankYouView.as_view(), name = 'external_invite_thankyou'),
]
