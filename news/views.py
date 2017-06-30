from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import permission_required
import datetime
from django.core.files import File
from PIL import Image
from lib.image import UploadToDirUUID
import os
from django.db.models.fields.files import ImageFieldFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


from news.models import NewsArticle
from fair.models import Fair
# Create your views here.

def resize_image(image, image_field, width, height):
    image = image.resize((width, height), Image.ANTIALIAS)
    filename = str(image_field)
    image_file = open(os.path.join('/tmp',filename), 'wb')
    image.save(image_file, 'JPEG', quality=120)
    image_file.close()

    image_data = open(os.path.join('/tmp',filename), 'rb')
    image_file = File(image_data)
    return image_file


class NewsArticleForm(forms.ModelForm):
    publication_date = forms.DateTimeField(initial=datetime.datetime.now)
    html_article_text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = NewsArticle
        fields = '__all__'
        exclude = ('image_2x', 'image_2x_wide', 'image')

    def save(self, *args, **kwargs):
        newsArticle = super(NewsArticleForm, self).save(*args, **kwargs)

        #back compatibility with field image
        newsArticle.image = newsArticle.image_3x_wide if newsArticle.image_3x_wide is not None else newsArticle.image_3x

        image_field = self.cleaned_data.get('image_3x')
        print(type(image_field))
        if type(image_field) == InMemoryUploadedFile or type(image_field) == TemporaryUploadedFile: # A new image has been uploaded in this field
            image = Image.open(image_field)
            w, h = image.size
            if w > 400: #This number should be reviewed. What should the width of small image be?
                image_file = resize_image(image, image_field, 200, 150)
                newsArticle.image_2x.save(str(image_field) + '_2x_.jpg', image_file)
            else:
                newsArticle.image_2x = newsArticle.image_3x
                newsArticle.save()


        image_field = self.cleaned_data.get('image_3x_wide')
        if type(image_field) == InMemoryUploadedFile or type(image_field) == TemporaryUploadedFile: # A new image has been uploaded in this field
            image = Image.open(image_field)
            w, h = image.size
            if w > 400: #This number should be reviewed. What should the width of small image be?
                image_file = resize_image(image, image_field, 266, 150)
                newsArticle.image_2x_wide.save(str(image_field) + '_2x_wide.jpg', image_file)
            else:
                newsArticle.image_2x_wide = newsArticle.image_3x_wide
                newsArticle.save()


    
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
        form.save()
        return redirect('news', year)
    return render(request, template_name, {'form':form, 'fair': fair})

@permission_required('news.change_newsarticle')
def news_article_update(request, year, pk, template_name='news/article_form.html'):
    fair = get_object_or_404(Fair, year=year)
    article = get_object_or_404(NewsArticle, pk=pk)
    form = NewsArticleForm(request.POST or None, request.FILES or None, instance=article)
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
