from django.conf.urls import url
from banquet.views import (
    ExternalInviteRedirectView,
    ExternalInviteCreateView,
    ExternalInviteUpdateView,
    ThankYouView,
)

from banquet import views

urlpatterns = [
	url(r'^afterparty$', views.external_banquet_afterparty, name = 'banquet_external_afterparty'),
	url(r'^afterparty/(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', views.external_banquet_afterparty, name = 'banquet_external_afterparty_token'),
	url(r'^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', views.external_invitation, name = 'banquet_external_invitation'),
	url(r'^(?P<token>[0-9A-Za-z]+)$', views.participant_display, name = 'banquet_participant_display'),
	url(r'^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/no$', views.external_invitation_no, name = 'banquet_external_invitation_no'),
	url(r'^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/maybe$', views.external_invitation_maybe, name = 'banquet_external_invitation_maybe')
]
