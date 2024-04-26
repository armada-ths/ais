from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.party_index, name="party_index"),
]

