from django.conf.urls import url

from . import api

app_name = "companies_api"

urlpatterns = [
    url(r"^$", api.companies),
    url(r"^registration_groups$", api.get_registration_groups),
]
