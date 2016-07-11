from django.contrib import admin

from django import forms
from tinymce.widgets import TinyMCE

from .models import NewsArticle


# used in order to set custom size for the WSIWYG-editor
class AdminTinyMCE(forms.ModelForm):
    html_article_text = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 20}))

    class Meta:
        model = NewsArticle
        fields = ("html_article_text", "title", "publication_date")

class NewsArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Content", {"fields": ["title", "html_article_text"]}),
        ("Publication time", {"fields": ["publication_date"]})
    ]

    form = AdminTinyMCE

    # List view
    list_display = ("title", "publication_date")

admin.site.register(NewsArticle, NewsArticleAdmin)