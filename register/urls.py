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
	url(r'^password/change', views.change_password, name='change_password'),
	url(r'^login/$', LoginView.as_view(template_name='register/login.html', authentication_form=LoginForm), name='login'),
	url(r'^logout/$', LogoutView.as_view(), name='logout'),
	url(r'^password_reset/$', PasswordResetView.as_view(
		template_name='register/outside/reset_password.html',
		form_class=ResetPasswordForm,
		email_template_name='register/outside/reset_password_email.html'), name='password_reset'),
	url(r'^password_reset/done/$', PasswordResetDoneView.as_view(template_name='register/outside/reset_password_done.html'), name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(
		template_name='register/outside/reset_password_confirm.html', 
		form_class=SetNewPasswordForm), name='password_reset_confirm'),

]
