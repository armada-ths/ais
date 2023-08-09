from django.conf.urls import url

from register.api import registration

app_name = "register_api"

urlpatterns = [
    url(r"^$", registration.index, name="index"),
    # url(r"^(?P<company_pk>[0-9]+)$", api.index, name="index"),
]
