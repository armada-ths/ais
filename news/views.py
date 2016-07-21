from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.forms import ModelForm
from django.forms import DateInput
from django.forms import DateTimeField
import datetime

from news.models import NewsArticle
# Create your views here.

class NewsArticleForm(ModelForm):
    publication_date = DateTimeField(initial=datetime.datetime.now)
    html_article_text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = NewsArticle
        fields = '__all__'
        widgets = {
            'publication_date': DateInput(attrs={'class':'datepicker'}),
        }


def news_list(request, template_name='news/news_list.html'):
    news = NewsArticle.objects.all()
    data = {}
    data['object_list'] = news
    return render(request, template_name, data)

def news_article_create(request, template_name='news/article_form.html'):
    form = NewsArticleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('news')
    return render(request, template_name, {'form':form})

