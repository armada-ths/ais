from ais.common.urls import *
from django.conf.urls import include, url
import djangosaml2

urlpatterns += [
    url(r'^login/', include('django.contrib.auth.urls'), name='login'),
    url(r'^logout/', include('django.contrib.auth.urls'), name='logout'),
]
