from django.conf.urls import url
from . import views

app_name = "people"

urlpatterns = [
    url(r"^$", views.list_people, name="list"),
    url(r"^edit$", views.edit, name="edit"),
    url(r"^(?P<pk>\d+)$", views.profile, name="profile"),
    url(r"^profile_delete/(?P<pk>\d+)$", views.profile_delete, name="profile_delete"),
]
