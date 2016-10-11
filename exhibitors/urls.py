from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.exhibitors, name='exhibitors'),
	url(r'^(?P<pk>\d+)/$', views.exhibitor, name='exhibitor'),
	url(r'^(?P<exhibitor_pk>\d+)/order/new$', views.order, name='order_new'),
	url(r'^(?P<exhibitor_pk>\d+)/order/(?P<order_pk>\d+)$', views.order, name='order'),
	url(r'^(?P<exhibitor_pk>\d+)/order/(?P<order_pk>\d+)/delete$', views.order_delete, name='order_delete'),
]