from django.conf.urls import url

from events import views

urlpatterns = [
    url(r'^$', views.event_list, name='event_list'),
    url(r'^new$', views.event_edit, name='event_new'),
    url(r'^(?P<pk>\d+)/signup$', views.event_attend_form, name='event_attend_form'),
    url(r'^(?P<pk>\d+)/edit', views.event_edit, name='event_edit'),
    url(r'^(?P<pk>\d+)/unattend$', views.event_unattend, name='event_unattend'),
    url(r'^(?P<pk>\d+)/attendants', views.event_attendants, name='event_attendants'),
]
