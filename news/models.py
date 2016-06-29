from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=150)
    html_text = models.CharField(max_length=5000)
    publication_date = models.DateTimeField()

    def __str__(self):
        return self.title
