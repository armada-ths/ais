from django.conf.urls import url
from . import views
from .models import BanquetteAttendant

urlpatterns = [
    url(r'^$', views.banquet_attendants, name='banquet'),
	url(r'^(?P<pk>\d+)/$', views.banquet_attendant, name='banquet'),

	url(r'^(?P<exhibitor_pk>\d+)/banquette_attendant/new$', views.related_object_form(BanquetteAttendant, 'Banquet attendant', 'banquette_attendant_delete'), name='banquette_attendant_new'),
	url(r'^(?P<exhibitor_pk>\d+)/banquette_attendant/(?P<instance_pk>\d+)$', views.related_object_form(BanquetteAttendant, 'Banquet attendant', 'banquette_attendant_delete'), name='banquette_attendant'),
	url(r'^(?P<exhibitor_pk>\d+)/banquette_attendant/(?P<instance_pk>\d+)/delete$', views.related_object_delete(BanquetteAttendant), name='banquette_attendant_delete'),

	url(r'^(?P<exhibitor_pk>\d+)/contact/(?P<instance_pk>\d+)$', views.related_object_form(Contact, 'Contact', None), name='contact'),
]
