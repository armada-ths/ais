from django.conf.urls import url

from banquet import api

app_name = 'banquet_api'

urlpatterns = [
    url(r'^(?P<banquet_pk>[0-9]+)/seats/(?P<seat_pk>[0-9]+)$', api.save_seat)
]
