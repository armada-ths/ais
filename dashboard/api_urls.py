from django.conf.urls import url

from .api.registration import registration

app_name = "dashboard_api"

urlpatterns = [
    url(r"^$", registration.index),
    url(r"^sign_ir$", registration.sign_ir),
    url(r"^submit$", registration.sign_cr),
    url(r"^(?P<company_pk>[0-9]+)$", registration.get_company),
]
