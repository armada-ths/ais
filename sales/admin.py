from django.contrib import admin

from .models import Sale, SaleComment, FollowUp 

# Register your models here.
admin.site.register(Sale)
admin.site.register(SaleComment)
admin.site.register(FollowUp)
