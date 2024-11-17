from django.conf.urls import url

from banquet import views
from banquet.views import ParticipantsListView, SendInviteCreateView, export_invitations

urlpatterns = [
    url(r"^$", views.dashboard, name="banquet_dashboard"),
    url(
        r"^invitation/(?P<token>[0-9A-Fa-f-]+)$",
        views.invitation,
        name="banquet_invitation",
    ),
    url(
        r"^invitation/(?P<token>[0-9A-Fa-f-]+)/no$",
        views.invitation_no,
        name="banquet_invitation_no",
    ),
    url(
        r"^invitation/(?P<token>[0-9A-Fa-f-]+)/maybe$",
        views.invitation_maybe,
        name="banquet_invitation_maybe",
    ),
    url(r"^(?P<banquet_pk>[0-9]+)$", views.manage, name="banquet_manage"),
    url(r"^(?P<banquet_pk>[0-9]+)/map$", views.manage_map, name="banquet_manage_map"),
    url(
        r"^(?P<banquet_pk>[0-9]+)/invitations$",
        views.manage_invitations,
        name="banquet_manage_invitations",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/invitations/(?P<invitation_pk>[0-9]+)$",
        views.manage_invitation,
        name="banquet_manage_invitation",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/invitations/(?P<invitation_pk>[0-9]+)/edit$",
        views.manage_invitation_form,
        name="banquet_manage_invitation_edit",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/invitations/new$",
        views.manage_invitation_form,
        name="banquet_manage_invitation_new",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/invitations/import$",
        views.manage_import_invitations,
        name="banquet_import_invitations",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/email$",
        views.manage_handle_email,
        name="banquet_handle_email",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/participants$",
        views.manage_participants,
        name="banquet_manage_participants",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/afterparty$",
        views.afterparty,
        name="afterparty",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/participants/exportafterparty$",
        views.export_afterparty,
        name="banquet_export_afterparty",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/participants/export$",
        views.export_participants,
        name="banquet_export_participants",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/participants/(?P<participant_pk>[0-9]+)$",
        views.manage_participant,
        name="banquet_manage_participant",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/participants/(?P<participant_pk>[0-9]+)/edit$",
        views.manage_participant_form,
        name="banquet_manage_participant_edit",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/participants/(?P<participant_pk>[0-9]+)/remove$",
        views.manage_participant_remove,
        name="banquet_manage_participant_remove",
    ),
    url(
        r"^(?P<banquet_pk>[0-9]+)/invitations/(?P<invitation_pk>[0-9]+)/mail_sent$",
        views.send_invitation_button,
        name="banquet_send_invitation_button",
    ),
    url(r"^participants$", ParticipantsListView.as_view(), name="participant_list"),
    url(r"^send$", SendInviteCreateView.as_view(), name="send_invite"),
    url(r"^export$", export_invitations, name="export_invitations"),
    url(
        r"^scan_tickets/(?P<banquet_pk>[0-9]+)$",
        views.scan_tickets,
        name="scan_tickets",
    ),
]
