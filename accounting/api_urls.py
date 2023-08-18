from django.conf.urls import url

from accounting import api

app_name = "accounting_api"

urlpatterns = [
    url(r"^products$", api.list_products),
]
