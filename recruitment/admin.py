from django.contrib import admin
from .models import RecruitmentPeriod, RecruitableRole, RecruitmentApplication, RoleApplication


class RecruitableRoleInline(admin.TabularInline):
    model = RecruitableRole

class RecruitmentPeriodAdmin(admin.ModelAdmin):
    inlines = [RecruitableRoleInline]

class RoleApplicationInline(admin.TabularInline):
    model = RoleApplication

class RecruitmentApplicationAdmin(admin.ModelAdmin):
    inlines = [RoleApplicationInline]

admin.site.register(RecruitmentPeriod, RecruitmentPeriodAdmin)
admin.site.register(RecruitmentApplication, RecruitmentApplicationAdmin)
