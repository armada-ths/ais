from django.conf.urls import url

from unirel import views

urlpatterns = [
    url(r"^$", views.admin, name="unirel_admin"),
    url(
        r"^dietary-restrictions$",
        views.admin_dietary_restrictions,
        name="unirel_admin_dietary_restrictions",
    ),
    url(r"^new$", views.admin_participant_form, name="unirel_admin_participant_new"),
    url(
        r"^(?P<participant_pk>[0-9]+)/delete$",
        views.admin_participant_delete,
        name="unirel_admin_participant_delete",
    ),
    url(
        r"^(?P<participant_pk>[0-9]+)/edit$",
        views.admin_participant_form,
        name="unirel_admin_participant_edit",
    ),
    url(
        r"^(?P<participant_pk>[0-9]+)$",
        views.admin_participant,
        name="unirel_admin_participant",
    ),
]
