from django.conf.urls import url

from . import api

app_name = "register_api"

urlpatterns = [
    url(
        r"^company_contact$", api.create_company_contact, name="create_company_contact"
    ),
]
