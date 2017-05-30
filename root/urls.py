from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    #url(r'^banquet_signup$', views.banquette_signup, name='banquette_signup'),
    #url(r'^banquet_signup_delete$', views.banquette_signup_delete, name='banquette_signup_delete'),
    url(r'^banquet_attendants', views.banquet_attendants, name='banquet_attendants'),
]
