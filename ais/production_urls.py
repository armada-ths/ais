from ais.common_urls import *
from django.conf.urls import include, url
from cas import views as cas_views

urlpatterns = +=[
    url(r'^login/', cas_views.login, name='login'),
]
