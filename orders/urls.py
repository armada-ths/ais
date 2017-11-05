from django.conf.urls import url
from orders import views

urlpatterns = [
    url(r'^$', views.products, name='products'),
    url(r'^(?P<pk>\d+)$', views.product, name='product'),
]
