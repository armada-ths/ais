from django.conf.urls import url

from . import views

app_name = 'fair'

urlpatterns = [
	url(r'^$', views.index, name = 'home'),
	url(r'^lunchtickets$', views.lunchtickets, name = 'lunchtickets')
]
