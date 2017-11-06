from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'matching'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^slidersgrading/', views.init_choosen_sliders_gradings, name='slider_grading'),
    url(r'^mapsweden/', views.map_sweden, name='map_sweden'),
    url(r'^map_world/', views.map_world, name='map_world'),
    url(r'^init_workfields/', views.init_workfields, name='init_workfields'),
    url(r'^finalize_workfields/', views.finalize_workfields, name='finalize_workfields'),
    url(r'^test/(?P<total>\d+)/$', views.test_matching, name='test_matching'),
]
