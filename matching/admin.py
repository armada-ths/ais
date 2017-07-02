from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Question, Survey, Response, TextAns, ChoiceAns, IntegerAns, BooleanAns

class QuestionInline(admin.ModelAdmin):
    list_display=('text', 'question_type')

class AnswerInline(admin.StackedInline):
    fields = ('question', 'ans')

class TextAnsInline(AnswerInline):
    model = TextAns

class ChoiceAnsInline(AnswerInline):
    model = ChoiceAns

class IntegerAnsInline(AnswerInline):
    model = IntegerAns

class BooleanAnsInline(AnswerInline):
    model = BooleanAns

class ResponseAdmin(admin.ModelAdmin):
    #note: one response only have one question and one answer that has the correct type! so be careful when you add in admin (maybe remove the ans inline)
    list_display = ('exhibitor', 'question')
    inlines = [TextAnsInline, ChoiceAnsInline, IntegerAnsInline, BooleanAnsInline]

admin.site.register(Question, QuestionInline)
admin.site.register(Survey)
admin.site.register(Response, ResponseAdmin)
admin.site.register(TextAns)
admin.site.register(ChoiceAns)
admin.site.register(IntegerAns)
admin.site.register(BooleanAns)
