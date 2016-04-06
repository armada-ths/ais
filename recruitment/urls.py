from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.recruitment, name='recruitment'),
    url(r'^new$', views.recruitment_period_new, name='recruitment_period_new'),
    url(r'^(?P<pk>\d+)/application/new$', views.recruitment_application_new, name='recruitment_application_new'),
    url(r'^application/(?P<pk>\d+)$', views.recruitment_application_delete, name='recruitment_application_delete'),
    url(r'^(?P<pk>\d+)$', views.recruitment_period, name='recruitment_period'),
]