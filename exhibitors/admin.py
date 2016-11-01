from django.contrib import admin

from .models import Exhibitor, WorkField, JobType, \
    Continent, Value, CatalogInfo, Location, BanquetteAttendant


@admin.register(CatalogInfo)
class CatalogInfoAdmin(admin.ModelAdmin):
    search_fields = ('display_name',)
    ordering = ('display_name',)
    fieldsets = (
        (None, {
            'fields': ('exhibitor', 'display_name', 'slug', 'short_description',
                       'description', 'employees_sweden', 'employees_world',
                       'countries', 'website_url', 'facebook_url',
                       'twitter_url', 'linkedin_url',)
        }),
        ('Images', {
            'classes': ('collapse',),
            'fields': ('logo_original', 'logo_small', 'logo_small_preview', 'logo', 'logo_preview', 'ad_original', 'ad',
                       'ad_preview',)
        }),
        ('Details', {
            'classes': ('collapse',),
            'fields': ('programs', 'main_work_field', 'work_fields',
                       'job_types', 'continents', 'values', 'tags',)
        })
    )
    readonly_fields = ('logo_small', 'logo', 'ad', 'logo_small_preview', 'logo_preview', 'ad_preview',)

    def logo_small_preview(self, instance):
        return '<img src="%s" />' % instance.logo_small.url

    logo_small_preview.allow_tags = True
    logo_small_preview.short_description = "Preview of small logo"

    def logo_preview(self, instance):
        return '<img src="%s" />' % instance.logo.url

    logo_preview.allow_tags = True
    logo_preview.short_description = "Preview of logo"

    def ad_preview(self, instance):
        return '<img src="%s" />' % instance.ad.url

    ad_preview.allow_tags = True
    ad_preview.short_description = "Preview of ad"


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
