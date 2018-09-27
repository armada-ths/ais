from django.conf.urls import url

from events import api

app_name = 'events_api'

urlpatterns = [
    url(r'^$', api.index, name='index'),
    url(r'^(?P<event_pk>\d+)$', api.show, name='show'),
    url(r'^(?P<event_pk>\d+)/payment$', api.payment, name='payment'),
    url(r'^(?P<event_pk>\d+)/signup$', api.signup, name='signup'),
]
