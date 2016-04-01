from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.recruitment, name='recruitment'),
    url(r'^new$', views.recruitment_period_new, name='recruitment_period_new'),

]
