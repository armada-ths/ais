from django.shortcuts import render
from news.models import NewsArticle
# Create your views here.

def news_list(request, template_name='news/news_list.html'):
    news = NewsArticle.objects.all()
    data = {}
    data['object_list'] = news
    return render(request, template_name, data)
