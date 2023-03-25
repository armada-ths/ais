from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LoginView, LogoutView

app_name = "accounts"

urlpatterns = [
    # url(r'^login/$', views.login, name='login'),
    url(
        r"^login/$",
        LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    url(r"^logout/$", LogoutView.as_view(), name="logout"),
    # url(r'^logout$', views.logout, name='logout'),
    # signup for externals
    url(
        r"^external/create_account$",
        views.external_create_account,
        name="external_create_account",
    ),
    # login for externals
    url(r"^external/login$", views.external_login, name="external_login"),
]
