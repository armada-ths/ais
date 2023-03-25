from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.news_article_list, name="news"),
    url(r"^(?P<pk>\d+)$", views.news_article_show, name="article_show"),
    url(r"^(?P<pk>\d+)/edit$", views.news_article_update, name="article_edit"),
    url(r"^new$", views.news_article_create, name="article_create"),
    url(r"^(?P<pk>\d+)/delete$", views.news_article_delete, name="article_delete"),
]
