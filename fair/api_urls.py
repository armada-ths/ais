from django.conf.urls import url

from fair import api

app_name = 'fair_api'

urlpatterns = [
    url(r'^lunchtickets/search$', api.lunchtickets_search, name='lunchtickets_search'),
]
