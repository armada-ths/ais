from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.list_people, name='list_people'),
    url(r'^(?P<user_id)>[0-9]+)$', views.view_person, name='view_person'),
]
