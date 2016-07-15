from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone


# Manager for getting only the articles that should be displayed
class NewsArticleManager(models.Manager):
    def get_queryset(self):
        return super(NewsArticleManager, self).get_queryset().filter(publication_date__lte=timezone.now())

class NewsArticle(models.Model):
    title = models.CharField(max_length=150)
    html_article_text = HTMLField(default="")
    publication_date = models.DateTimeField()

    def __str__(self):
        return self.title

    objects = models.Manager() # keep the default manager
    public_articles = NewsArticleManager() # add custom manager