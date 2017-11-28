from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import  static
urlpatterns = [
    url(r'^$', views.recruitment, name='recruitment'),
    url(r'^assign_roles$', views.assign_roles, name='assign_roles'),
    url(r'^(?P<pk>\d+)$', views.recruitment_period, name='recruitment_period'),
    url(r'^(?P<pk>\d+)/interview_state_counts$', views.interview_state_counts, name='interview_state_counts'),
    url(r'^(?P<pk>\d+)/graphs$', views.recruitment_period_graphs, name='recruitment_period_graphs'),

    url(r'^roles/new$', views.roles_new, name='roles_new'),

    url(r'^roles/(?P<pk>\d+)/delete$', views.roles_delete, name='roles_delete'),
    url(r'^roles/(?P<pk>\d+)$', views.roles_new, name='roles_new'),

    url(r'^(?P<pk>\d+)/edit$', views.recruitment_period_edit, name='recruitment_period_edit'),
    url(r'^new$', views.recruitment_period_edit, name='recruitment_period_new'),
    url(r'^(?P<pk>\d+)/delete$', views.recruitment_period_delete, name='recruitment_period_delete'),
    url(r'^(?P<recruitment_period_pk>\d+)/application/new$', views.recruitment_application_new, name='recruitment_application_new'),
    url(r'^(?P<recruitment_period_pk>\d+)/application/(?P<pk>\d+)$', views.recruitment_application_new, name='recruitment_application_new'),

# Disabled at the moment since the permissions aren't working as they should (2017-11-27). Because of this, the recruitment app is not working at all.
# Tests are disabled as well.
#    url(r'^(?P<recruitment_period_pk>\d+)/application/(?P<pk>\d+)/interview$', views.recruitment_application_interview,
#        name='recruitment_application_interview'),

    url(r'^(\d+)/application/(?P<pk>\d+)/delete$', views.recruitment_application_delete, name='recruitment_application_delete'),


    url(r'^(\d+)/application/(?P<pk>\d+)/comment$', views.recruitment_application_comment_new,
        name='recruitment_application_comment_new'),



]
