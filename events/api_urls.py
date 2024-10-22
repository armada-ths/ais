from django.conf.urls import url

from events import api

app_name = "events_api"

urlpatterns = [
    url(r"^$", api.index, name="index"),
    url(r"^(?P<event_pk>\d+)$", api.show, name="show"),
    url(
        r"^(?P<event_pk>\d+)/check_in/(?P<participant_pk>\d+)$",
        api.check_in,
        name="check_in",
    ),
    url(
        r"^(?P<event_pk>\d+)/check_out/(?P<participant_pk>\d+)$",
        api.check_out,
        name="check_out",
    ),
    url(
        r"^(?P<event_pk>\d+)/get_by_token/(?P<check_in_token>\w+)$",
        api.get_by_token,
        name="get_by_token",
    ),
    url(r"^(?P<event_pk>\d+)/payment$", api.payment, name="payment"),
    url(r"^(?P<event_pk>\d+)/signup$", api.signup, name="signup"),
    url(r"^(?P<event_pk>\d+)/upload$", api.upload_file, name="upload"),
    url(r"^(?P<event_pk>\d+)/teams/create$", api.create_team, name="create_team"),
    url(r"^(?P<event_pk>\d+)/teams/leave$", api.leave_team, name="leave_team"),
    url(r"^(?P<event_pk>\d+)/teams/(?P<team_pk>\d+)$", api.join_team, name="join_team"),
    url(
        r"^(?P<event_pk>\d+)/teams/(?P<team_pk>\d+)/update$",
        api.update_team,
        name="update_team",
    ),
    url(
        r"^(?P<event_pk>\d+)/deregister/(?P<participant_pk>\d+)$",
        api.deregister,
        name="deregister",
    ),
    url(
        r"^(?P<event_pk>\d+)/participants/fetch_details$",
        api.fetch_participants_details,
        name="fetch_participants_details",
    ),
]
