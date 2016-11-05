from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.root),
    url(r'^exhibitors/', views.exhibitors),
    url(r'^events/', views.events),
    url(r'^news/', views.news),
    url(r'^partners/', views.partners),
    url(r'^organization/', views.organization),
    url(r'^status/$', views.status),
]
