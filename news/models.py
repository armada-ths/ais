from django.db import models
from django.utils import timezone
from django.core.files import File
from lib.image import UploadToDirUUID
from PIL import Image
import io

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
    image_3x_wide = models.ImageField(
        upload_to = UploadToDirUUID('news', 'image'),
        verbose_name = 'Wide image (16:9) ratio',
        blank = True,
    )
    image_2x_wide = models.ImageField(
        upload_to = UploadToDirUUID('news', 'image'),
        blank = True,
    )
    image_3x = models.ImageField(
        upload_to = UploadToDirUUID('news', 'image'),
        verbose_name = 'Regular image (4:3) ratio',
        blank = True,
    )
    image_2x = models.ImageField(
        upload_to = UploadToDirUUID('news', 'image'),
        blank = True,
    )

    def __str__(self):
        return self.title

    
    objects = models.Manager() # keep the default manager
    public_articles = NewsArticleManager() # add custom manager
