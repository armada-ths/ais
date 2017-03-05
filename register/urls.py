from django.conf.urls import url
from . import views

app_name = 'anmalan'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^fair$', views.fair, name='fair'),
    url(r'^fair/(?P<fair_id>\d+)/signup$', views.prel_registration, name='prel_registration'),
    url(r'^company/(?P<pk>\d+)/edit', views.company_update, name='edit_company'),
]
