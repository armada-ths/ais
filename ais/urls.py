"""ais URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    #admin
    url(r'^admin/', include(admin.site.urls)),

    #login logout
    url(r'^login/$', 'cas.views.login', name='login'),
    url(r'^logout/$', 'cas.views.logout', name='logout'),

    # Root
    url(r'^$', include('root.urls')),

    # Events
    url(r'^events/', include('events.urls')),

    # Companies
    url(r'^companies/', include('companies.urls')),
    
    # People
    #url(r'^people/', include('people.urls')),
    


]
