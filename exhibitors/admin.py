from django.contrib import admin

from .models import Exhibitor, WorkField, JobType, Continent, Value, CatalogInfo

# Register your models here.
admin.site.register(Exhibitor)
admin.site.register(WorkField)
admin.site.register(JobType)
admin.site.register(Continent)
admin.site.register(Value)
admin.site.register(CatalogInfo)
