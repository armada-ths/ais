from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views
from .forms import LoginForm

app_name = 'anmalan'
urlpatterns = [
    url(r'^home$', views.home, name='home'),
    url(r'^$', views.index, name='index'),
    url(r'^company/(?P<pk>\d+)/edit', views.company_update, name='edit_company'),
    url(r'^me/edit', views.contact_update, name='edit_me'),
    url(r'^signup', views.signup, name='create_company_user'),
    url(r'^new_company', views.create_company, name='create_company'),
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

]
