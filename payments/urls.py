from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import  static

urlpatterns = [
    url(r'^checkout$', views.checkout, name='checkout'),
    url(r'^confirm$', views.confirm, name='confirm'),
]
