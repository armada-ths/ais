from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.companies_list, name = 'companies_list'),
	url(r'^new$', views.companies_form, name = 'companies_new'),
	url(r'^(?P<pk>\d+)/edit$', views.companies_form, name = 'companies_edit'),
	url(r'^(?P<pk>\d+)$', views.companies_view, name = 'companies_view'),
]
