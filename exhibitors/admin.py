from django.contrib import admin

from .models import Exhibitor, WorkField, JobType, \
    Continent, Value, CatalogInfo, Location, BanquetteAttendant
from lib.util import image_preview

import csv
from django.http import HttpResponse


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


def export_banquet_attendants_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=event.csv'

    csv_headers = [
        'First name', 'Last name', 'Email', 'Gender', 'Phone number',
        'Allergies', 'Alcohol', 'Lactose free', 'Gluten free', 'Vegetarian'
    ]

    writer = csv.writer(response)
    writer.writerow(csv_headers)
    for attendant in queryset:
        writer.writerow([
            attendant.first_name, attendant.last_name, attendant.email, attendant.gender, attendant.phone_number,
            attendant.allergies, attendant.wants_alcohol, attendant.wants_lactose_free_food, attendant.wants_gluten_free_food, attendant.wants_vegetarian_food
        ])
    return response

@admin.register(BanquetteAttendant)
class BanquetAdmin(admin.ModelAdmin):
    actions = [export_banquet_attendants_as_csv]


admin.site.register(WorkField)
admin.site.register(JobType)
admin.site.register(Continent)
admin.site.register(Value)
admin.site.register(Location)
