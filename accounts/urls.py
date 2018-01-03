from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import  static

#from djangosaml2.views import login
from django.contrib.auth.views import login, logout

urlpatterns = [
    #url(r'^login/$', views.login, name='login'),
    url(
        r'^login/$',
        login,
        name='login',
        kwargs={'template_name': 'accounts/login.html'}
    ),
    url(
        r'^logout/$',
        logout,
        name='logout',
        kwargs={'next_page': '/'}
    ),
    #url(r'^logout$', views.logout, name='logout'),
]
