from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('root.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^locations/', include('locations.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^people/', include('people.urls')),
    url(r'^recruitment/', include('recruitment.urls')),
    url(r'^exhibitors/', include('exhibitors.urls')),
    url(r'^products/', include('orders.urls')),
    url(r'^companies/', include('companies.urls')),
    url(r'^accounting/', include('accounting.urls')),
    url(r'^banquet/', include('banquet.urls')),
]
