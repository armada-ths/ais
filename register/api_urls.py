from django.conf.urls import url

from register.api import registration

app_name = "register_api"

urlpatterns = [
    url(r"^$", registration.index),
    url(r"^submit$", registration.submit),
    url(r"^(?P<company_pk>[0-9]+)$", registration.get_company),
]
