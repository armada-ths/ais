from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import permission_required
import datetime

from news.models import NewsArticle
# Create your views here.

class NewsArticleForm(forms.ModelForm):
    publication_date = forms.DateTimeField(initial=datetime.datetime.now)
    html_article_text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = NewsArticle
        fields = '__all__'

    
def news_article_list(request, template_name='news/article_list.html'):
    news = {}
    if request.user.has_perm('news.change_newsarticle'):
    	news = NewsArticle.objects.values('id', 'title', 'publication_date')
    else:
        news = NewsArticle.public_articles.values('id', 'title', 'publication_date')
    data = {}
    data['object_list'] = news
    
    return render(request, template_name, data)


@permission_required('news.add_newsarticle')
def news_article_create(request, template_name='news/article_form.html'):
    form = NewsArticleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('news')
    return render(request, template_name, {'form':form})

@permission_required('news.change_newsarticle')
def news_article_update(request, pk, template_name='news/article_form.html'):
    article = get_object_or_404(NewsArticle, pk=pk)
    form = NewsArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('news')
    return render(request, template_name, {'form':form})

def news_article_show(request, pk, template_name='news/article_show.html'):
    article = get_object_or_404(NewsArticle, pk=pk)
    return render(request, template_name, {'article':article})

@permission_required('news.delete_newsarticle')
def news_article_delete(request, pk, template_name='news/article_delete.html'):
    article = get_object_or_404(NewsArticle, pk=pk)
    if request.method=='POST':
        article.delete()
        return redirect('news')
    return render(request, template_name, {'article':article})
