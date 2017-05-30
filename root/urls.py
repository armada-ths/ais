from django.conf.urls import url
from django.contrib.auth.views import password_reset_confirm
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    #url(r'^banquet_signup$', views.banquette_signup, name='banquette_signup'),
    #url(r'^banquet_signup_delete$', views.banquette_signup_delete, name='banquette_signup_delete'),
    url(r'^banquet_attendants', views.banquet_attendants, name='banquet_attendants'),
    url(r'^logout/reset/(?P<uidb46>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        name='password_reset_confirm',
        kwargs={'template_name': 'root/reset_password_confirm.html',
                'post_reset_redirect': 'anmalan:login'}
    ),
]
