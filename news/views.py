from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import permission_required
import datetime

from news.models import NewsArticle
from fair.models import Fair
# Create your views here.

class NewsArticleForm(forms.ModelForm):
    publication_date = forms.DateTimeField(initial=datetime.datetime.now)
    html_article_text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = NewsArticle
        fields = '__all__'

    
def news_article_list(request, year, template_name='news/article_list.html'):
    fair = get_object_or_404(Fair, year=year)
    news = {}
    if request.user.has_perm('news.change_newsarticle'):
    	news = NewsArticle.objects.values('id', 'title', 'publication_date')
    else:
        news = NewsArticle.public_articles.values('id', 'title', 'publication_date')
    return render(request, template_name, {'object_list': news, 'fair':fair})


@permission_required('news.add_newsarticle')
def news_article_create(request, year, template_name='news/article_form.html'):
    fair = get_object_or_404(Fair, year=year)
    form = NewsArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('news', year)
    return render(request, template_name, {'form':form, 'fair': fair})

@permission_required('news.change_newsarticle')
def news_article_update(request, year, pk, template_name='news/article_form.html'):
    fair = get_object_or_404(Fair, year=year)
    article = get_object_or_404(NewsArticle, pk=pk)
    form = NewsArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('news', year)
    return render(request, template_name, {'form':form, 'fair':fair})

def news_article_show(request, year, pk, template_name='news/article_show.html'):
    fair = get_object_or_404(Fair, year=year)
    article = get_object_or_404(NewsArticle, pk=pk)
    return render(request, template_name, {'article':article, 'fair':fair})

@permission_required('news.delete_newsarticle')
def news_article_delete(request, year, pk, template_name='news/article_delete.html'):
    fair = get_object_or_404(Fair, year=year)
    article = get_object_or_404(NewsArticle, pk=pk)
    if request.method=='POST':
        article.delete()
        return redirect('news', year)
    return render(request, template_name, {'article':article, 'fair': fair})
