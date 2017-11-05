from django.contrib import admin

import csv
from django.http import HttpResponse
from .models import SignupContract, SignupLog, OrderLog

def export_signup_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=exhibitors.csv'

    csv_headers = [
        'company', 'contact',
        'contact_email', 'contact_cell_phone', 'contact_work_phone', 
    ]

    writer = csv.writer(response)
    writer.writerow(csv_headers)
    for signup in queryset:
        csv_row = [
            signup.company.name,
            signup.contact.name,
            signup.contact.email,
            signup.contact.cell_phone,
            signup.contact.work_phone,
        ]

        writer.writerow(csv_row)

    return response

# Overrides admin register to add custom actions
@admin.register(SignupLog)
class SignupLogAdmin(admin.ModelAdmin):
    search_fields = ('company__name', 'timestamp')
    ordering = ('-timestamp',)
    list_filter = ('type', )

    actions = [export_signup_as_csv]

@admin.register(OrderLog)
class OrderLogAdmin(admin.ModelAdmin):
    search_fields = ('company__name', 'timestamp',)
    ordering = ('-timestamp',)
    list_filter = ('action', 'fair')

# Register your models here.
admin.site.register(SignupContract)
