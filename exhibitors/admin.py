from django.contrib import admin

from .models import Exhibitor, WorkField, JobType, \
    Continent, Value, CatalogInfo, Location
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
        'requests_for_stand_placement', 'requests_for_exhibition_area',
        'interested_in_armada_transport',
        'transport_to_fair_type', 'number_of_packages_to_fair', 'number_of_pallets_to_fair',
        'estimated_arrival',
        'transport_from_fair_type', 'number_of_packages_from_fair',
        'number_of_pallets_from_fair',
        'transport_from_fair_address', 'transport_from_fair_zip_code', 'transport_from_fair_recipient_name',
        'transport_from_fair_recipient_phone_number',
        'heavy_duty_electric_equipment', 'other_information_about_the_stand',
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
            exhibitor.requests_for_stand_placement,
            exhibitor.requests_for_exhibition_area,

            exhibitor.interested_in_armada_transport,
            exhibitor.transport_to_fair_type,
            exhibitor.number_of_packages_to_fair,
            exhibitor.number_of_pallets_to_fair,
            exhibitor.estimated_arrival,

            exhibitor.transport_from_fair_type,
            exhibitor.number_of_packages_from_fair,
            exhibitor.number_of_pallets_from_fair,

            exhibitor.transport_from_fair_address,
            exhibitor.transport_from_fair_zip_code,
            exhibitor.transport_from_fair_recipient_name,
            exhibitor.transport_from_fair_recipient_phone_number,

            exhibitor.heavy_duty_electric_equipment,
            exhibitor.other_information_about_the_stand,
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
    list_filter = ('status', 'requests_for_stand_placement', 'requests_for_exhibition_area', 'transport_to_fair_type', 'transport_from_fair_type', 'fair',)

    actions = [export_exhibitor_as_csv]


admin.site.register(WorkField)
admin.site.register(JobType)
admin.site.register(Continent)
admin.site.register(Value)
admin.site.register(Location)
