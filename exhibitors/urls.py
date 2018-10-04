from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.exhibitors, name='exhibitors'),
	url(r'^(?P<pk>\d+)$', views.exhibitor, name = 'exhibitor'),
	url(r'^(?P<pk>\d+)/transport$', views.exhibitor_transport, name = 'exhibitor_transport'),
	url(r'^(?P<pk>\d+)/contact_persons$', views.exhibitor_contact_persons, name = 'exhibitor_contact_persons'),
	url(r'view$', views.edit_view, name = 'edit_view'),
	url(r'create$', views.create, name = 'create'),
]
