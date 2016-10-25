from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^banquette_signup$', views.banquette_signup, name='banquette_signup'),
    url(r'^banquette_signup_delete$', views.banquette_signup_delete, name='banquette_signup_delete'),
]
