from django.contrib import admin

from .models import Exhibitor, WorkField, JobType, \
    Continent, Value, CatalogInfo, Location, BanquetteAttendant


@admin.register(CatalogInfo)
class CatalogInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('exhibitor', 'display_name', 'slug', 'short_description',
                       'description', 'employees_sweden', 'employees_world',
                       'countries', 'website_url', 'facebook_url',
                       'twitter_url', 'linkedin_url',)
        }),
        ('Images', {
            'classes': ('collapse',),
            'fields': ('logo_original', 'logo_small', 'logo', 'ad_original', 'ad',)
        }),
        ('Details', {
            'classes': ('collapse',),
            'fields': ('programs', 'main_work_field', 'work_fields',
                       'job_types', 'continents', 'values', 'tags',)
        })
    )
    readonly_fields = ('logo_small', 'logo', 'ad',)


# Register your models here.
admin.site.register(Exhibitor)
admin.site.register(WorkField)
admin.site.register(JobType)
admin.site.register(Continent)
admin.site.register(Value)
admin.site.register(Location)
admin.site.register(BanquetteAttendant)
