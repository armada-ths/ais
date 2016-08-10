from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import  static
urlpatterns = [
    #url(r'^login/$', views.login, name='login'),
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        name='login',
        kwargs={'template_name': 'accounts/login.html'}
    ),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        name='logout',
        kwargs={'next_page': '/'}
    ),
    #url(r'^logout$', views.logout, name='logout'),
]
