from django.conf.urls import url

from events import views

app_name = "events"

urlpatterns = [
    url(r"^$", views.event_list, name="event_list"),
    url(r"^new$", views.event_new, name="event_new"),
    url(r"^(?P<pk>\d+)$", views.event_edit, name="event_edit"),
    url(r"^(?P<event_pk>\d+)/teams$", views.team_new, name="team_new"),
    url(r"^(?P<event_pk>\d+)/check_in$", views.check_in, name="check_in"),
    url(
        r"^(?P<event_pk>\d+)/teams/(?P<team_pk>\d+)$", views.team_edit, name="team_edit"
    ),
    url(r"^(?P<event_pk>\d+)/signup$", views.event_signup, name="event_signup"),
]
