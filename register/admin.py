from django.contrib import admin

from django.http import HttpResponse
from .models import SignupContract, SignupLog

# Overrides admin register to add custom actions
@admin.register(SignupLog)
class SignupLogAdmin(admin.ModelAdmin):
    search_fields = ('company__name', 'timestamp')
    ordering = ('-timestamp',)
    list_filter = ('type', )

# Register your models here.
admin.site.register(SignupContract)
