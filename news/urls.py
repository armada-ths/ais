from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.news_list, name='news'),
    url(r'^new$', views.news_article_create, name='news_article_new'),
]
