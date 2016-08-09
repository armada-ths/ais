from django.conf.urls import include, url
from django.contrib import admin
from ais.common import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('root.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
    url(r'^companies/', include('companies.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^locations/', include('locations.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^people/', include('people.urls')),
    url(r'^recruitment/', include('recruitment.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = 'AIS administration'
admin.site.site_header = 'AIS administration'
admin.site.index_title = 'AIS administration'
