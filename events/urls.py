from django.conf.urls import url

from events import views

app_name = 'events'

urlpatterns = [
    url(r'^$', views.list_events, name='list_events'),
    url(r'^new$', views.event_new, name='event_new')
]
