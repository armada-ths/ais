from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'matching'
urlpatterns = [
    url(r'^test/(?P<total>\d+)/$', views.test_matching, name='matching'),
]
