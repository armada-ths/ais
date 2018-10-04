from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.companies_list, name = 'companies_list'),
	url(r'^new$', views.companies_new, name = 'companies_new'),
	url(r'^slack_call$', views.companies_slack_call, name = 'companies_slack_call'),
	url(r'^statistics$', views.statistics, name = 'statistics'),
	url(r'^groups$', views.groups, name = 'groups_list'),
	url(r'^groups/new$', views.groups, name = 'groups_new'),
	url(r'^groups/(?P<pk>\d+)$', views.groups, name = 'groups_edit'),
	url(r'^contracts/export$', views.contracts_export, name = 'contracts_export'),
	url(r'^(?P<pk>\d+)$', views.companies_view, name = 'companies_view'),
	url(r'^(?P<pk>\d+)/details$', views.companies_details, name = 'companies_details'),
	url(r'^(?P<pk>\d+)/edit$', views.companies_edit, name = 'companies_edit'),
	url(r'^(?P<pk>\d+)/edit/groups/(?P<group_pk>\d+)$', views.companies_edit, name = 'companies_edit_groups'),
	url(r'^(?P<pk>\d+)/edit/responsibles/(?P<responsible_group_pk>\d+)$', views.companies_edit, name = 'companies_edit_responsibles_edit'),
	url(r'^(?P<pk>\d+)/edit/responsibles/(?P<responsible_group_pk>\d+)/remove$', views.companies_edit_responsibles_remove, name = 'companies_edit_responsibles_remove'),
	url(r'^(?P<pk>\d+)/orders/new$', views.companies_orders_new, name = 'companies_orders_new'),
	url(r'^(?P<pk>\d+)/orders/(?P<order_pk>\d+)$', views.companies_orders_edit, name = 'companies_orders_edit'),
	url(r'^(?P<pk>\d+)/orders/(?P<order_pk>\d+)/remove$', views.companies_orders_remove, name = 'companies_orders_remove'),
	url(r'^(?P<pk>\d+)/comments/(?P<comment_pk>\d+)/edit$', views.companies_comments_edit, name = 'companies_comments_edit'),
	url(r'^(?P<pk>\d+)/comments/(?P<comment_pk>\d+)/remove$', views.companies_comments_remove, name = 'companies_comments_remove'),
	url(r'^(?P<pk>\d+)/contacts/(?P<contact_pk>\d+)/edit$', views.companies_contacts_edit, name = 'companies_contacts_edit')
]
