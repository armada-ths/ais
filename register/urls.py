from django.conf.urls import url
from django.contrib.auth.views import (
        LoginView, LogoutView, PasswordResetView, 
        PasswordResetDoneView,PasswordResetConfirmView)
from . import views
from .forms import LoginForm, ResetPasswordForm, SetNewPasswordForm

app_name = 'anmalan'

""" For physical fair, add following lines to urlpatterns below:
	url(r'^(?P<company_pk>[0-9]+)/transport$', views.transport, name = 'transport'),
	url(r'^(?P<company_pk>[0-9]+)/lunchtickets$', views.lunchtickets, name = 'lunchtickets'),
	url(r'^(?P<company_pk>[0-9]+)/lunchtickets/new$', views.lunchtickets_form, name = 'lunchtickets_new'),
	url(r'^(?P<company_pk>[0-9]+)/lunchtickets/(?P<lunch_ticket_pk>[0-9]+)$', views.lunchtickets_form, name = 'lunchtickets_edit'),
	url(r'^(?P<company_pk>[0-9]+)/banquet$', views.banquet, name = 'banquet'),
	url(r'^(?P<company_pk>[0-9]+)/banquet/new$', views.banquet_form, name = 'banquet_new'),
	url(r'^(?P<company_pk>[0-9]+)/banquet/(?P<banquet_participant_pk>[0-9]+)$', views.banquet_form, name = 'banquet_edit'),
"""

urlpatterns = [
	url(r'^$', views.choose_company, name = 'choose_company'),
	url(r'^(?P<company_pk>[0-9]+)/registration$', views.form, name = 'registration'),
	url(r'^(?P<company_pk>[0-9]+)/events$', views.events, name = 'events'),
	url(r'^user', views.create_user, name = 'create_user'),
	url(r'^company', views.create_company, name = 'create_company'),
	url(r'^login/$', LoginView, name='login', kwargs={'template_name': 'register/login.html', 'authentication_form': LoginForm }),
	url(r'^logout/$', LogoutView, name='logout', kwargs={'next_page': 'anmalan:index'}),
	url(r'^password/change', views.change_password, name='change_password'),
	url(r'^password_reset/$', PasswordResetView, name='password_reset', kwargs={'template_name': 'register/outside/reset_password.html', 'password_reset_form': ResetPasswordForm, 'post_reset_redirect': 'anmalan:password_reset_done', 'email_template_name': 'register/outside/reset_password_email.html'}),
	url(r'^password_reset/done/$', PasswordResetDoneView, name='password_reset_done', kwargs={'template_name': 'register/outside/reset_password_done.html'}),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView, name='password_reset_confirm', kwargs={'template_name': 'register/outside/reset_password_confirm.html', 'set_password_form': SetNewPasswordForm, 'post_reset_redirect': '/register/login'})
]
