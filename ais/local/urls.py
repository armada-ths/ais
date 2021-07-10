from ais.common.urls import *
from django.conf.urls import include, url
from cas import views as cas_views
from kth_login import views as kth_login_views

urlpatterns += [
    url(r'^login/', kth_login_views.kth_login, name='login'),
    url(r'^oidc/kth/callback$', kth_login_views.authorize, name='authorize'),
]
