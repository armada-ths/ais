from django.conf.urls import url

from exhibitors import api

app_name = 'exhibitors_api'

urlpatterns = [
	url(r'^$', api.exhibitors),
	url(r'^locations$', api.locations),
	url(r'^locations/(?P<location_pk>[0-9]+)$', api.location),
	url(r'^days$', api.days),
]
