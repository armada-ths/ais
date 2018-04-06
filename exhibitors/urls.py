from django.conf.urls import url
from . import views
from banquet.models import BanquetteAttendant
from orders.models import Order
from companies.models import CompanyContact

urlpatterns = [
    url(r'^$', views.exhibitors, name='exhibitors'),
	url(r'^(?P<pk>\d+)/$', views.exhibitor, name='exhibitor'),

    url(r'view$', views.edit_view, name='edit_view'),

	url(r'^(?P<pk>\d+)/emails_confirmation/$', views.emails_confirmation, name='emails_confirmation'),
	url(r'^(?P<pk>\d+)/send_cr_receipts$', views.send_cr_receipts, name='send_cr_receipts'),
	url(r'^(?P<pk>\d+)/send_emails/$', views.send_emails, name='send_emails'),

	url(r'^(?P<exhibitor_pk>\d+)/order/new$', views.related_object_form(Order,'Order', 'order_delete'), name='order_new'),
	url(r'^(?P<exhibitor_pk>\d+)/order/(?P<instance_pk>\d+)$', views.related_object_form(Order, 'Order', 'order_delete'), name='order'),
	url(r'^(?P<exhibitor_pk>\d+)/order/(?P<instance_pk>\d+)/delete$', views.related_object_delete(Order), name='order_delete'),

	url(r'^(?P<exhibitor_pk>\d+)/banquette_attendant/new$', views.related_object_form(BanquetteAttendant, 'Banquet attendant', 'banquette_attendant_delete'), name='banquette_attendant_new'),
	url(r'^(?P<exhibitor_pk>\d+)/banquette_attendant/(?P<instance_pk>\d+)$', views.related_object_form(BanquetteAttendant, 'Banquet attendant', 'banquette_attendant_delete'), name='banquette_attendant'),
	url(r'^(?P<exhibitor_pk>\d+)/banquette_attendant/(?P<instance_pk>\d+)/delete$', views.related_object_delete(BanquetteAttendant), name='banquette_attendant_delete'),

	url(r'^(?P<exhibitor_pk>\d+)/contact/(?P<instance_pk>\d+)$', views.related_object_form(CompanyContact, 'Contact', None), name='contact'),
]
