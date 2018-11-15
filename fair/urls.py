from django.conf.urls import url

from . import views

app_name = 'fair'

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^tickets$', views.tickets, name='tickets'),
    url(r'^check_in$', views.lunchtickets_check_in, name='lunchtickets_check_in'),
    url(r'^lunchtickets$', views.lunchtickets, name='lunchtickets'),
    url(r'^lunchtickets/create$', views.lunchticket_create, name='lunchticket_create'),
    url(r'^lunchtickets/(?P<token>[A-Za-z0-9]+)$', views.lunchticket, name='lunchticket'),
    url(r'^lunchtickets/(?P<token>[A-Za-z0-9]+)/remove$', views.lunchticket_remove, name='lunchticket_remove'),
]
