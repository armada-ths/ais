from django.contrib import admin

from .models import Sale, SaleComment, FollowUp, BuisnessArea

# Register your models here.
admin.site.register(Sale)
admin.site.register(SaleComment)
admin.site.register(FollowUp)
admin.site.register(BuisnessArea)
