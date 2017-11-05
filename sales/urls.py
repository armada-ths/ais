from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.sales_list, name='sales'),
    url(r'^(?P<pk>\d+)$', views.sale_show, name='sale_show'),
    url(r'^(?P<pk>\d+)/edit$', views.sale_edit, name='sale_edit'),
    url(r'^new$', views.sale_edit, name='sale_create'),
    url(r'^import$', views.import_companies, name='sale_import'),
    url(r'^(?P<pk>\d+)/delete$', views.sale_delete, name='sale_delete'),
    url(r'^(?P<pk>\d+)/comment/new$', views.sale_comment_create, name='sale_comment_create'),
    url(r'^(?P<sale_pk>\d+)/comment/(?P<comment_pk>\d+)/delete$', views.sale_comment_delete, name='sale_comment_delete'),
]
