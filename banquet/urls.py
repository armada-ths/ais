from django.conf.urls import url
from banquet.views import (
    InternalInviteView,
    ExternalInviteView,
    SentInvitationsListView,
    SendInviteCreateView
)

from django.conf import settings
from django.conf.urls.static import  static

urlpatterns = [
	url(r'^internal_invite/$', InternalInviteView.as_view(), name = 'internal_invite'),
	url(r'^invite/$', ExternalInviteView.as_view(), name = 'external_invite'),
	url(r'^$', SentInvitationsListView.as_view(), name = 'invite_list'),
	url(r'^send/$', SendInviteCreateView.as_view(), name = 'send_invite'),
]
