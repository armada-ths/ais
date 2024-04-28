from django.conf.urls import include, url
from django.contrib import admin
from ais.common import settings
from django.conf.urls.static import static
from fair.views import login_redirect
from testpage.views import testpage
from exhibitors.views import UserAutocomplete
from magic_link import urls as magic_link_urls

urlpatterns = [
    url(r"^party/", include("party.urls")),
    url(r"^accounts/", include("accounts.urls")),
    url(r"^admin/", admin.site.urls),
    url(r"^companies/", include("companies.urls")),
    url(r"^register/", include("register.urls")),
    url(r"^dashboard/", include("dashboard.urls")),
    url(r"^api/", include("api.urls")),
    url(r"^banquet/", include("banquet.urls")),
    url(r"^$", login_redirect),
    url(r"^fairs/", include("urls.urls")),
    url(r"^journal/", include("journal.urls")),
    url(r"^banquet/", include("banquet.urls_external")),
    url(r"^unirel/", include("unirel.urls_external")),
    url(r"^", include("fair.urls_external")),
    url(r"^testpage/", include("testpage.urls")),
    url(r"^payments/", include("payments.urls")),
    url(r"^hijack/", include("hijack.urls")),
    url(r"^magic_link/", include(magic_link_urls)),
    url(
        r"^user-autocomplete/$",
        UserAutocomplete.as_view(),
        name="user-autocomplete",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = "AIS administration"
admin.site.site_header = "AIS administration"
admin.site.index_title = "AIS administration"
