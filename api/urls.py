from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.root),
    url(r'^events/', include('events.api_urls')),
    url(r'^exhibitors/', include('exhibitors.api_urls')),
    url(r'^fair/', include('fair.api_urls')),
    url(r'^catalogueselections/', views.catalogueselections),
    url(r'^news/', views.news),
    url(r'^organization/', views.organization),
    url(r'^partners/', views.partners),
    url(r'^questions/?$', views.questions),
    url(r'^recruitment/$', views.recruitment),
    url(r'^status/$', views.status),
    url(r'^student_profile$', views.student_profile),
    url(r'^matching/$', views.matching)
]
