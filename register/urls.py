from django.conf.urls import url
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm
from . import views
from .forms import LoginForm, ResetPasswordForm, SetNewPasswordForm

app_name = 'anmalan'
urlpatterns = [
    url(r'^home$', views.home, name='home'),
    url(r'^$', views.index, name='index',
        kwargs={'template_name': 'register/index.html'}),
    url(r'^submitted/$', views.submission_view, name='submitted'),
    url(r'^signup', views.signup, name='create_company_user'),
    url(r'^new_company', views.create_company, name='create_company'),

    # signup for externals
    #url(r'^external/signup$', views.external_signup, name='external/signup'),
    # login for externals
    #url(r'^external/login$', views.external_login, name='external_login'),

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

    url(r'^password_reset/$',
        password_reset,
        name='password_reset',
        kwargs={'template_name': 'register/reset_password.html',
                'password_reset_form': ResetPasswordForm,
                'post_reset_redirect': 'anmalan:password_reset_done',
                'email_template_name': 'register/reset_password_email.html'}
    ),
    url(r'^password_reset/done/$',
        password_reset_done,
        name='password_reset_done',
        kwargs={'template_name': 'register/reset_password_done.html'}
    ),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        name='password_reset_confirm',
        kwargs={'template_name': 'register/reset_password_confirm.html',
                'set_password_form': SetNewPasswordForm,
                'post_reset_redirect': '/register/external/login'}
    ),
]
