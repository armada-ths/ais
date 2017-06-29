from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Question, Survey, Response, TextAns, ChoiceAns, IntegerAns, BooleanAns, Category

class QuestionInline(admin.TabularInline):
    model = Question
    ordering = ('name',)

class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline,]

class AnswerInline(admin.StackedInline):
    fields = ('question', 'ans')
    readonly_fields = ('question',)

class TextAnsInline(AnswerInline):
    model = TextAns

class ChoiceAnsInline(AnswerInline):
    model = ChoiceAns

class IntegerAnsInline(AnswerInline):
    model = IntegerAns

class BooleanAnsInline(AnswerInline):
    model = BooleanAns

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('exhibitor',)
    inlines = [TextAnsInline, ChoiceAnsInline, IntegerAnsInline, BooleanAnsInline]
    readonly_fields = ('survey', 'exhibitor')

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
#admin.site.register(ChoiceAns)
#admin.site.register(TextAns)
#admin.site.register(BooleanAns)
#admin.site.register(Question)
