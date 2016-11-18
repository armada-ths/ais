from django.contrib import admin

from .models import SalesPeriod, Campaign, Sale, SaleComment, FollowUp 

# Register your models here.
admin.site.register(SalesPeriod)
admin.site.register(Campaign)
admin.site.register(Sale)
admin.site.register(SaleComment)
admin.site.register(FollowUp)
