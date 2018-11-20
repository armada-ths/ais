from django.conf.urls import url

from banquet import api

app_name = 'banquet_api'

urlpatterns = [
    url(r'^(?P<banquet_pk>[0-9]+)/seats/(?P<seat_pk>[0-9]+)$', api.save_seat),
    url(r'^tickets/search$', api.ticket_search, name='ticket_search'),
    url(r'^tickets/check_in/(?P<ticket_pk>\d+)$', api.ticket_check_in, name='ticket_check_in'),
    url(r'^tickets/check_out/(?P<ticket_pk>\d+)$', api.ticket_check_out, name='ticket_check_out'),
    url(r'^tickets/check_in_by_token$', api.ticket_check_in_by_token, name='ticket_check_in_by_token'),
]
