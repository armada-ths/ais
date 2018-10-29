from django.conf.urls import url

from unirel import views

urlpatterns = [
	url(r'^$', views.admin, name = 'unirel_admin'),
	url(r'^new$', views.admin_participant_form, name = 'unirel_admin_participant_new'),
	url(r'^(?P<participant_pk>[0-9]+)/edit$', views.admin_participant_form, name = 'unirel_admin_participant_edit'),
	url(r'^(?P<participant_pk>[0-9]+)$', views.admin_participant, name = 'unirel_admin_participant'),
	url(r'^(?P<token>[0-9A-Fa-f\\-]+)$', views.register, name = 'unirel_register')
]
