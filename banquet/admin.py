from django.contrib import admin

from .models import BanquetteAttendant, BanquetTable, BanquetTicket
from django.contrib.auth.models import User
from exhibitors.models import Exhibitor
from fair.models import Fair
from lib.util import image_preview

import csv
from django.http import HttpResponse

def export_banquet_attendants_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=banquet_attendants.csv'

    csv_headers = [
        'Fair ID',
        'First name',
        'Last name',
        'Email',
        'Ticket Type',
        'Table',
        'Gender',
        'Phone number',
        'Allergies',
        'Alcohol',
        'Lactose free',
        'Gluten free',
        'Vegan',
        'Job Title',
        'Linkedin URL',
        'Confirmed',
        'Table ID',
        'Ignored from placement',
        'Seat Number'

    ]

    writer = csv.writer(response)
    writer.writerow(csv_headers)
    print("QUERY SET", queryset, modeladmin, request)
    for attendant in queryset:
        writer.writerow([
            attendant.fair_id,
            attendant.first_name,
            attendant.last_name,
            attendant.email,
            attendant.ticket,
            attendant.table,
            attendant.gender,
            attendant.phone_number,
            attendant.allergies,
            attendant.wants_alcohol,
            attendant.wants_lactose_free_food,
            attendant.wants_gluten_free_food,
            attendant.wants_vegan_food,
            attendant.job_title,
            attendant.linkedin_url,
            attendant.confirmed,
            attendant.table_id,
            attendant.ignore_from_placement,
            attendant.seat_number
        ])
    return response

@admin.register(BanquetteAttendant)
class BanquetAdmin(admin.ModelAdmin):
    actions = [export_banquet_attendants_as_csv]
    search_fields = ('first_name', 'last_name')

@admin.register(BanquetTable)
class BanquetAdmin(admin.ModelAdmin):
    search_fields = ('table_name',)

@admin.register(BanquetTicket)
class BanquetAdmin(admin.ModelAdmin):
    search_fields = ('name',)
