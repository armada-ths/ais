from django.contrib import admin
from .models import RecruitmentPeriod, RecruitableRole, RecruitmentApplication, RoleApplication, InterviewQuestion, InterviewQuestionAnswer, InterviewQuestionFieldArgument

class RecruitableRoleInline(admin.TabularInline):
    model = RecruitableRole

class InterviewQuestionInline(admin.TabularInline):
    model = InterviewQuestion

class InterviewQuestionAnswerInline(admin.TabularInline):
    model = InterviewQuestionAnswer

class InterviewQuestionFieldArgumentInline(admin.TabularInline):
    model = InterviewQuestionFieldArgument

class InterviewQuestionAdmin(admin.ModelAdmin):

    inlines = [InterviewQuestionFieldArgumentInline]

class RecruitmentPeriodAdmin(admin.ModelAdmin):
    inlines = [RecruitableRoleInline, InterviewQuestionInline]

class RoleApplicationInline(admin.TabularInline):
    model = RoleApplication

class RecruitmentApplicationAdmin(admin.ModelAdmin):
    inlines = [RoleApplicationInline, InterviewQuestionAnswerInline]

admin.site.register(RecruitmentPeriod, RecruitmentPeriodAdmin)
admin.site.register(RecruitmentApplication, RecruitmentApplicationAdmin)
admin.site.register(InterviewQuestion, InterviewQuestionAdmin)
