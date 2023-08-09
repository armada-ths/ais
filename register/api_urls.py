from django.conf.urls import url

from register import api

app_name = "register_api"

urlpatterns = [
    url(r"^$", api.index, name="index"),
    # url(r"^(?P<company_pk>[0-9]+)$", api.index, name="index"),
]
