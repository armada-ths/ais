from django.conf.urls import url

from events import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/signup$', views.event_attend_form, name='event_attend_form'),
    url(r'^(?P<pk>\d+)/unattend$', views.event_unattend, name='event_unattend'),
]
