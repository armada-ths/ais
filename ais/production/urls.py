from ais.common.urls import *
from django.conf.urls import include, url
#from cas import views as cas_views
from djangosaml2 import views as saml_views

urlpatterns +=[
    #url(r'^login/', cas_views.login, name='login'),
    url(r'^login/', saml_views.login, name='login'),
]
