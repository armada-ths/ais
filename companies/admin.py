from django.contrib import admin

from .models import Company, CompanyContact, CompanyParticipationYear

# Register your models here.
admin.site.register(Company)
admin.site.register(CompanyContact)
admin.site.register(CompanyParticipationYear)
