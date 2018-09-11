from django.contrib import admin

from .models import *
from lib.util import image_preview

import csv
from django.http import HttpResponse
from orders.models import Order, Product


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
                       'ad_original', 'ad_preview', 'location_at_fair_original', 'location_at_fair',
                       'location_at_fair_preview',)
        }),
        ('Details', {
            'classes': ('collapse',),
            'fields': ('programs', 'main_work_field', 'work_fields',
                       'job_types', 'continents', 'values', 'tags',)
        })
    )
    readonly_fields = ('logo_small_preview', 'logo_preview', 'ad_preview', 'location_at_fair_preview',)

    logo_small_preview = image_preview('logo_small')
    logo_preview = image_preview('logo')
    ad_preview = image_preview('ad')
    location_at_fair_preview = image_preview('location_at_fair')


def export_exhibitor_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=exhibitors.csv'

    csv_headers = [
        'company', 'stand_location',
    ]

    # the list of products is not fair specific
    for product in Product.objects.all():
        prodName = product.name + ' (' + str(product.fair.year) + ')'
        csv_headers.append(prodName)

    writer = csv.writer(response)
    writer.writerow(csv_headers)
    for exhibitor in queryset:
        csv_row = [
            exhibitor.company.name,
            exhibitor.location.name if exhibitor.location else '',
        ]

        for product in Product.objects.all():
            order = Order.objects.filter(exhibitor=exhibitor, product=product).first()
            csv_row.append(order.amount if order else 0)

        writer.writerow(csv_row)

    return response


@admin.register(Exhibitor)
class ExhibitorAdmin(admin.ModelAdmin):
    search_fields = ('company__name',)
    # order by fair in first hand
    ordering = ('-fair__year', 'company',)
    # filters to filter search query
    list_filter = ['fair']

    actions = [export_exhibitor_as_csv]


admin.site.register(CatalogueIndustry)
admin.site.register(CatalogueValue)
admin.site.register(CatalogueEmployment)
admin.site.register(CatalogueLocation)
admin.site.register(CatalogueBenefit)
