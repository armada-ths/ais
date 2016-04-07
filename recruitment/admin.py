from django.contrib import admin
from .models import RecruitmentPeriod, RecruitableRole, RecruitmentApplication, RoleApplication, InterviewQuestion, InterviewQuestionAnswer


class RecruitableRoleInline(admin.TabularInline):
    model = RecruitableRole

class InterviewQuestionInline(admin.TabularInline):
    model = InterviewQuestion

class InterviewQuestionAnswerInline(admin.TabularInline):
    model = InterviewQuestionAnswer

class RecruitmentPeriodAdmin(admin.ModelAdmin):
    inlines = [RecruitableRoleInline, InterviewQuestionInline]

class RoleApplicationInline(admin.TabularInline):
    model = RoleApplication

class RecruitmentApplicationAdmin(admin.ModelAdmin):
    inlines = [RoleApplicationInline, InterviewQuestionAnswerInline]

admin.site.register(RecruitmentPeriod, RecruitmentPeriodAdmin)
admin.site.register(RecruitmentApplication, RecruitmentApplicationAdmin)
