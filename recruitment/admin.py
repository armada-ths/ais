from django.contrib import admin
from .models import RecruitmentPeriod, RoleForRecruitmentPeriod


class RoleForRecruitmentPeriodInline(admin.TabularInline):
    model = RoleForRecruitmentPeriod

class RecruitmentPeriodAdmin(admin.ModelAdmin):
    inlines = [
        RoleForRecruitmentPeriodInline,
    ]

admin.site.register(RecruitmentPeriod, RecruitmentPeriodAdmin)
admin.site.register(RoleForRecruitmentPeriod)
