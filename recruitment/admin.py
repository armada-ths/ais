from django.contrib import admin
from .models import RecruitmentPeriod, RecruitableRole


class RecruitableRoleInline(admin.TabularInline):
    model = RecruitableRole

class RecruitmentPeriodAdmin(admin.ModelAdmin):
    inlines = [
        RecruitableRoleInline,
    ]

admin.site.register(RecruitmentPeriod, RecruitmentPeriodAdmin)
