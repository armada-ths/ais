from django.contrib import admin
from .models import RecruitmentPeriod, RecruitableRole, RecruitmentApplication, RoleApplication, ExtraField, CustomField, CustomFieldAnswer, CustomFieldArgument

class RecruitableRoleInline(admin.TabularInline):
    model = RecruitableRole

class CustomFieldInline(admin.TabularInline):
    model = CustomField

class CustomFieldAnswerInline(admin.TabularInline):
    model = CustomFieldAnswer

class CustomFieldArgumentInline(admin.TabularInline):
    model = CustomFieldArgument

class CustomFieldAdmin(admin.ModelAdmin):
    inlines = [CustomFieldArgumentInline]

class RecruitmentPeriodAdmin(admin.ModelAdmin):
    inlines = [RecruitableRoleInline]

class RoleApplicationInline(admin.TabularInline):
    model = RoleApplication

class RecruitmentApplicationAdmin(admin.ModelAdmin):
    inlines = [RoleApplicationInline]

admin.site.register(RecruitmentPeriod, RecruitmentPeriodAdmin)
admin.site.register(RecruitmentApplication, RecruitmentApplicationAdmin)
admin.site.register(CustomField, CustomFieldAdmin)

#admin.site.register(ExtraField)
#admin.site.register(CustomField)
