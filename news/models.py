from django.db import models
from tinymce.models import HTMLField

class NewsArticle(models.Model):
    title = models.CharField(max_length=150)
    html_article_text = HTMLField(default="")
    publication_date = models.DateTimeField()

    def __str__(self):
        return self.title
