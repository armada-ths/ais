from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.exhibitors, name="exhibitors"),
    url(r"^(?P<pk>\d+)$", views.exhibitor, name="exhibitor"),
    url(
        r"^(?P<pk>\d+)/transport$",
        views.exhibitor_transport,
        name="exhibitor_transport",
    ),
    url(r"^(?P<pk>\d+)/details$", views.exhibitor_details, name="exhibitor_details"),
    url(
        r"^(?P<pk>\d+)/coordinates$",
        views.exhibitor_coordinates,
        name="exhibitor_coordinates",
    ),
    url(
        r"^(?P<pk>\d+)/fair_location$",
        views.exhibitor_fair_location,
        name="exhibitor_fair_location",
    ),
    url(
        r"^(?P<pk>\d+)/application_status$",
        views.exhibitor_application_status,
        name="exhibitor_application_status",
    ),
    url(
        r"^(?P<pk>\d+)/contact_persons$",
        views.exhibitor_contact_persons,
        name="exhibitor_contact_persons",
    ),
    url(r"^(?P<pk>\d+)/check_in$", views.exhibitor_check_in, name="exhibitor_check_in"),
    url(
        r"^(?P<pk>\d+)/check_in/revert$",
        views.exhibitor_check_in_revert,
        name="exhibitor_check_in_revert",
    ),
    url(
        r"^(?P<pk>\d+)/comments/(?P<comment_pk>\d+)/edit$",
        views.exhibitor_comment_edit,
        name="exhibitor_comment_edit",
    ),
    url(
        r"^(?P<pk>\d+)/comments/(?P<comment_pk>\d+)/remove$",
        views.exhibitor_comment_remove,
        name="exhibitor_comment_remove",
    ),
    url(r"^view$", views.edit_view, name="edit_view"),
    url(r"^create$", views.create, name="create"),
    url(r"^export$", views.export, name="export"),
    url(
        r"^people_count/(?P<location_pk>[0-9]+)$",
        views.people_count,
        name="people_count",
    ),
]
