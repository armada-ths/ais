from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.sales_list, name='sales'),
    url(r'^(?P<pk>\d+)$', views.sale_show, name='sale_show'),
    url(r'^(?P<pk>\d+)/edit$', views.sale_edit, name='sale_edit'),
    url(r'^new$', views.sale_create, name='sale_create'),
    url(r'^(?P<pk>\d+)/delete$', views.sale_delete, name='sale_delete'),
]