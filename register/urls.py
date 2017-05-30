from django.conf.urls import url
from django.contrib.auth.views import login, logout, password_reset, password_reset_done
from . import views
from .forms import LoginForm

app_name = 'anmalan'
urlpatterns = [
    url(r'^home$', views.home, name='home'),
    # Initial registration closed, to allow: rm kwargs and uncomment signup and create_company, also uncomment in templates/register/login.html
    url(r'^$', views.index, name='index',
        kwargs={'template_name': 'register/index-post-register-deadline.html'}),
    url(r'^company/(?P<pk>\d+)/edit', views.company_update, name='edit_company'),
    url(r'^me/edit', views.contact_update, name='edit_me'),
    # url(r'^signup', views.signup, name='create_company_user'),
    # url(r'^new_company', views.create_company, name='create_company'),
    url(
        r'^login/$',
        login,
        name='login',
        kwargs={'template_name': 'register/login.html', 'authentication_form':LoginForm }
    ),
    url(
        r'^logout/$',
        logout,
        name='logout',
        kwargs={'next_page': 'anmalan:index'}
    ),
    url(r'^password/change', views.change_password, name='change_password'),
    #urls for resetting password
    url(r'^password_reset/$',
        password_reset,
        name='password_reset',
        kwargs={'template_name': 'register/reset_password.html',
                'post_reset_redirect': 'anmalan:password_reset_done'}
    ),
    url(r'^password_reset/done/$',
        password_reset_done,
        name='password_reset_done',
        kwargs={'template_name': 'register/reset_password_done.html'}
    ),
]
