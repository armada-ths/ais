from django.conf.urls import url
from . import views

urlpatterns = [
    #CRUD Company /company, /company/new, /company/edit/pk, /company/delete/pk
#    url(r'^$', views.companies_list, name='companies_list'),
#    url(r'^(?P<pk>\d+)$', views.list_company, name='company'),
#    url(r'^new$', views.company_create, name='company_new'),
#    url(r'^edit/(?P<pk>\d+)$', views.company_update, name='company_edit'),
#    url(r'^delete/(?P<pk>\d+)$', views.company_delete, name='company_delete'),
    #CRUD Company contact person
#    url(r'^(?p<pk>\d+)/new$', views.contact_create, name='contact_new'),
    url(r'^contact/(?P<contact_pk>\d+)/toggle_active$', views.contact_state_toggle, 
        name='contact_state_toggle'),

]
