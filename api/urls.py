from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r"^$", views.root),
    url(r"^events/", include("events.api_urls")),
    url(r"^exhibitors/", include("exhibitors.api_urls")),
    url(r"^banquet/", include("banquet.api_urls")),
    url(r"^fair/", include("fair.api_urls")),
    url(r"^dashboard/", include("dashboard.api_urls")),
    url(r"^accounting/", include("accounting.api_urls")),
    url(r"^catalogueselections/", views.catalogueselections),
    url(r"^news/", views.news),
    url(r"^organization/v2", views.organization_v2),
    url(r"^organization/", views.organization),
    url(r"^create_magic_link/", views.create_magic_link, name="create_magic_link"),
    url(r"^partners/", views.partners),
    url(r"^questions/?$", views.questions),
    url(r"^recruitment/$", views.recruitment),
    url(r"^recruitment_data/$", views.recruitment_data),
    url(r"^dates/$", views.dates),
    url(r"^student_profile$", views.student_profile),
    url(r"^matching/$", views.matching),
    url(r"^matching/choices$", views.matching_choices),
    url(r"^companies", views.companies),
]
