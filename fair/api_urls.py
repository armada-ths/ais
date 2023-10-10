from django.conf.urls import url

from fair import api

app_name = "fair_api"

urlpatterns = [
    url(r"^lunchtickets/search$", api.lunchtickets_search, name="lunchtickets_search"),
    url(r"^lunchtickets/companysearch$", api.lunchtickets_companysearch, name="lunchtickets_companysearch"),
    url(
        r"^lunchtickets/check_in/(?P<lunch_ticket_pk>\d+)$",
        api.lunchticket_check_in,
        name="lunchtickets_check_in",
    ),
    url(
        r"^lunchtickets/check_out/(?P<lunch_ticket_pk>\d+)$",
        api.lunchticket_check_out,
        name="lunchtickets_check_out",
    ),
    url(
        r"^lunchtickets/check_in_by_token$",
        api.lunchticket_check_in_by_token,
        name="lunchtickets_check_in_by_token",
    ),
]
