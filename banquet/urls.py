from django.conf.urls import url
from . import views
from .models import BanquetteAttendant

urlpatterns = [
    url(r'^$', views.banquet_attendants, name='banquet'),
	url(r'^attendant/(?P<pk>\d+)/$', views.banquet_attendant, name='banquet/attendant'),
	url(r'^attendant/new$', views.new_banquet_attendant, name='banquet/new'),
    url(r'^signup$', views.banquet_external_signup, name='banquet/signup'),
    url(r'^thankyou$', views.thank_you, name='banquet/thankyou'),
    url(r'^sit_attendants/$', views.sit_attendants, name='banquet/sit_attendants'),
    url(r'^placement$', views.table_placement, name='banquet/placement'),
]
