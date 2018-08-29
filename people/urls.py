from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)$', views.view_person, name='view_person'),
    url(r'^(?P<pk>\d+)/edit$', views.edit_person, name='edit_person'),
]
