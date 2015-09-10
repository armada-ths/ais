from django.conf.urls import url
from . import views

urlpatterns = [
    #companies
    url(r'^companies/$', views.companies_list, name='companies_list'),
    url(r'^companies/new$', views.company_create, name='company_new'),
    url(r'^companies/edit/(?P<pk>\d+)$', views.company_update, name='company_edit'),
    url(r'^companies/delete/(?P<pk>\d+)$', views.company_delete, name='company_delete'),
]
