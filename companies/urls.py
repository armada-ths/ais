from django.conf.urls import url
from . import views

urlpatterns = [
    #CRUD Company /company, /company/new, /company/edit/pk, /company/delete/pk
    url(r'^$', views.companies_list, name='companies_list'),
    # TODO url(r'^e(?P<pk>\d+)$', views.company_update, name='company_edit'), 
    url(r'^new$', views.company_create, name='company_new'),
    url(r'^edit/(?P<pk>\d+)$', views.company_update, name='company_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.company_delete, name='company_delete'),

    #CRUD Company contact person

]
