from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.root),
    url(r'^companies/', views.companies),
    url(r'^events/', views.events),
    url(r'^news/', views.news),
]
