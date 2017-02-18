from django.conf.urls import include, url
from django.contrib import admin
from ais.common import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^fairs/(?P<year>\d+)/', include('urls.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = 'AIS administration'
admin.site.site_header = 'AIS administration'
admin.site.index_title = 'AIS administration'
