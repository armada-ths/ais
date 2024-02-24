from django.conf.urls import url
from . import views

app_name = "dashboard"

urlpatterns = [
    url(
        r"^(?P<company_id>\d+)(?:.*)/?$",
        views.dashboard_company,
        name="company_dashboard",
    ),
    url(r"^(?:.*)/?$", views.dashboard_index, name="index"),
]
