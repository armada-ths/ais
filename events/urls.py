from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='events'),
    url(r'^new/$', views.event, name='events'),
]
