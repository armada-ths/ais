from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.exhibitors, name='exhibitors'),
	url(r'^(?P<pk>\d+)/$', views.exhibitor, name='exhibitor'),
	url(r'^(?P<pk>\d+)/product/$', views.exhibitor, name='exhibitor'),
]
