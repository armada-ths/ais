from django.conf.urls import url

from events import api

app_name = 'events_api'

urlpatterns = [
    url(r'^$', api.index, name='index'),
    url(r'^(?P<pk>\d+)$', api.show, name='show'),
]
