from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.list_people, name='list people'),
    url(r'^(?P<id>[0-9]+)$', views.view_person, name='view person'),
]
