from django.db import models
from django.utils import timezone

# Manager for getting only the articles that should be displayed
class NewsArticleManager(models.Manager):
    def get_queryset(self):
        return super(NewsArticleManager, self).get_queryset().filter(publication_date__lte=timezone.now())

class NewsArticle(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=50, blank=True)
    ingress = models.TextField(default="", max_length=500)
    html_article_text = models.TextField(default="", max_length=5000)
    publication_date = models.DateTimeField()
    image = models.ImageField(
        upload_to = 'news/image/',
        blank = True,
    )

    def __str__(self):
        return self.title

    objects = models.Manager() # keep the default manager
    public_articles = NewsArticleManager() # add custom manager
