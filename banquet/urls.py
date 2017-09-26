from django.conf.urls import url
from . import views
from .models import BanquetteAttendant

urlpatterns = [
    url(r'^$', views.banquet_attendants, name='banquet'),
	
]
