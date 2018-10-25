from django.conf.urls import url
from banquet.views import (
    ExternalInviteRedirectView,
    ExternalInviteCreateView,
    ExternalInviteUpdateView,
    ThankYouView,
)

from banquet import views

urlpatterns = [
	url(r'^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', views.external_invitation, name = 'banquet_external_invitation'),
	url(r'^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/no$', views.external_invitation_no, name = 'banquet_external_invitation_no'),
	url(r'^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/maybe$', views.external_invitation_maybe, name = 'banquet_external_invitation_maybe'),
]
