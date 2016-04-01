from django.conf.urls import patterns, url

from events import views

urlpatterns = [
  url(r'^$', views.event_list, name='event_list'),
  url(r'^new/$', views.event_create, name='event_new'),
  url(r'^attendence/$',views.event_create_attendence, name='event_new_attendence'),
  url(r'^show/$', views.event_attendence_list, name='event_attendence_list'),
  url(r'^edit/(?P<pk>\d+)$', views.event_update, name='event_edit'),
  url(r'^delete/(?P<pk>\d+)$', views.event_delete, name='event_delete'),
]
