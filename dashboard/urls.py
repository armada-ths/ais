from django.conf.urls import url
from . import views

app_name = "dashboard"

urlpatterns = [
    url(
        r"^register$",
        views.register_company_contact,
        name="register_company_contact",
    ),
    url(
        r"^(?P<company_id>\d+)(?:.*)/?$",
        views.company_dashboard,
        name="company_dashboard",
    ),
    url(r"^(?:.*)/?$", views.dashboard_index, name="index"),
]
