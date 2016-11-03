from django.contrib import admin

from .models import Exhibitor, WorkField, JobType, \
    Continent, Value, CatalogInfo, Location, BanquetteAttendant
from lib.util import image_preview


@admin.register(CatalogInfo)
class CatalogInfoAdmin(admin.ModelAdmin):
    search_fields = ('display_name',)
    ordering = ('display_name',)
    fieldsets = (
        (None, {
            'fields': ('exhibitor', 'display_name', 'slug',
                       'short_description', 'description', 'employees_sweden',
                       'employees_world', 'countries', 'website_url',
                       'facebook_url', 'twitter_url', 'linkedin_url',)
        }),
        ('Images', {
            'classes': ('collapse',),
            'fields': ('logo_original', 'logo_small_preview', 'logo_preview',
                       'ad_original', 'ad_preview',)
        }),
        ('Details', {
            'classes': ('collapse',),
            'fields': ('programs', 'main_work_field', 'work_fields',
                       'job_types', 'continents', 'values', 'tags',)
        })
    )
    readonly_fields = ('logo_small_preview', 'logo_preview', 'ad_preview',)

    logo_small_preview = image_preview('logo_small')
    logo_preview = image_preview('logo')
    ad_preview = image_preview('ad')


@admin.register(Exhibitor)
class ExhibitorAdmin(admin.ModelAdmin):
    search_fields = ('company__name',)
    ordering = ('company',)
    list_filter = ('status',)


admin.site.register(WorkField)
admin.site.register(JobType)
admin.site.register(Continent)
admin.site.register(Value)
admin.site.register(Location)
admin.site.register(BanquetteAttendant)
