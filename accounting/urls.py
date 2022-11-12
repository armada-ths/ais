from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.accounting, name = 'accounting'),
	url(r'^export_orders$', views.export_orders, name = 'export_orders'),
	url(r'^companies_without_ths_customer_ids$', views.companies_without_ths_customer_ids, name = 'companies_without_ths_customer_ids'),
	url(r'^product_summary$', views.product_summary, name = 'product_summary'),
	url(r'^export_company$', views.export_companys, name = 'export_company')
]
