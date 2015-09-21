from django.conf.urls import url
from . import views

urlpatters = [
    url(r'^$', views.list_people, name="List people"),
]
