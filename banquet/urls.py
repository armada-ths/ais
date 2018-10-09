from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import  static

from banquet.views import (
    InternalInviteRedirectView,
    InternalInviteCreateView,
    InternalInviteUpdateView,
    ParticipantsListView,
    SendInviteCreateView,
    ThankYouView,
    export_invitations
)
from banquet import views

urlpatterns = [
	url(r'^$', views.banquet_dashboard, name = 'banquet_dashboard'),
	url(r'^invitation/(?P<token>[0-9A-Fa-f-]+)$', views.banquet_invitation, name = 'banquet_invitation'),
	url(r'^(?P<banquet_pk>[0-9]+)$', views.banquet_manage, name = 'banquet_manage'),
	url(r'^(?P<banquet_pk>[0-9]+)/invitations$', views.banquet_manage_invitations, name = 'banquet_manage_invitations'),
	url(r'^(?P<banquet_pk>[0-9]+)/invitations/(?P<invitation_pk>[0-9]+)$', views.banquet_manage_invitation, name = 'banquet_manage_invitation'),
	url(r'^(?P<banquet_pk>[0-9]+)/invitations/(?P<invitation_pk>[0-9]+)/edit$', views.banquet_manage_invitation_form, name = 'banquet_manage_invitation_edit'),
	url(r'^(?P<banquet_pk>[0-9]+)/invitations/new$', views.banquet_manage_invitation_form, name = 'banquet_manage_invitation_new'),
	url(r'^(?P<banquet_pk>[0-9]+)/participants$', views.banquet_manage_participants, name = 'banquet_manage_participants'),
	url(r'^participants$', ParticipantsListView.as_view(), name = 'participant_list'),
	url(r'^send$', SendInviteCreateView.as_view(), name = 'send_invite'),
	url(r'^export$', export_invitations, name='export_invitations')
]
