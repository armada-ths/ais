from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.start, name = 'journal'),
	url(r'^ics/(?P<user_pk>\d+)/(?P<token>[0-9a-f\-]+)$', views.ics, name = 'journal_ics'),
]
