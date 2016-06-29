from django.contrib import admin

from .models import NewsArticle

class NewsArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Content", {"fields": ["title", "html_article_text"]}),
        ("Publication time", {"fields": ["publication_date"]})
    ]

    # List view
    list_display = ("title", "publication_date")

admin.site.register(NewsArticle, NewsArticleAdmin)