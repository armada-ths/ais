from django.conf.urls import include, url
from django.contrib import admin
from ais.common import settings
from django.conf.urls.static import static
from root.views import login_redirect

urlpatterns = [
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^companies/', include('companies.urls')),
    url(r'^register/', include('register.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^$', login_redirect),
    url(r'^fairs/(?P<year>\d+)/', include('urls.urls')),
    #url(r'^matching/', include('matching.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = 'AIS administration'
admin.site.site_header = 'AIS administration'
admin.site.index_title = 'AIS administration'
