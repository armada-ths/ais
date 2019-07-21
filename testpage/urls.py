from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import  static

urlpatterns = [
    url(r'^$', views.testpage, name='testpage'),
    url(r'^send_test_email$', views.send_test_email, name='send_test_email'),
]
