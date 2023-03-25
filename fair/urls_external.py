from django.conf.urls import url

from fair import views

urlpatterns = [
    url(
        r"^lunchticket/(?P<token>[A-Za-z0-9]+)$",
        views.lunchticket_display,
        name="lunchticket_display",
    )
]
