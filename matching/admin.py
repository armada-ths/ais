from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Question, Survey, Response, TextAns, ChoiceAns, IntegerAns, \
BooleanAns, StudentQuestionSlider, StudentQuestionGrading, StudentAnswerSlider, \
StudentAnswerGrading, WorkFieldArea, WorkField, StudentAnswerWorkField, SwedenRegion, \
Continent, StudentAnswerRegion, StudentAnswerContinent, SwedenCity, Country, JobType, \
StudentAnswerJobType, KNNClassifier, VectorKNN

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

class WorkFieldInline(admin.TabularInline):
    model = WorkField

class WorkFieldAreaAdmin(admin.ModelAdmin):
    list_display = ('work_area',)
    inlines = [WorkFieldInline]

class StudentAnswerWFieldInline(admin.TabularInline):
    list_display = ('student', 'work_field', 'answer')
    model = StudentAnswerWorkField

class WorkFieldAdmin(admin.ModelAdmin):
    list_display = ('work_field','work_area')
    inlines = [StudentAnswerWFieldInline]

class AnswerSliderAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'answer_min', 'answer_max')
    model = StudentAnswerSlider

class AnswerGradingAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'answer')
    model = StudentAnswerGrading

# Student Questions
class StudentQuestionSliderAdmin(admin.ModelAdmin):
    exclude = ('question_type',)
    model = StudentQuestionSlider

class StudentQuestionGradingAdmin(admin.ModelAdmin):
    exclude = ('question_type',)
    model = StudentQuestionGrading

class SwedenRegionAdmin(admin.ModelAdmin):
    model = SwedenRegion

class ContinentAdmin(admin.ModelAdmin):
    model = Continent

class SwedenCityAdmin(admin.ModelAdmin):
    model = SwedenCity

class StudentAnswerContinentAdmin(admin.ModelAdmin):
    model = StudentAnswerContinent

class StudentAnswerRegionAdmin(admin.ModelAdmin):
    model = StudentAnswerRegion

class CountryAdmin(admin.ModelAdmin):
    model = Country

class JobTypeAdmin(admin.ModelAdmin):
    model = JobType

class StudentAnswerJobTypeAdmin(admin.ModelAdmin):
    model = StudentAnswerJobType

class KNNVectorInline(admin.TabularInline):
    list_display = ('exhibitor', 'vector', 'classifer')
    model = VectorKNN

class KNNClassifierAdmin(admin.ModelAdmin):
    inlines = [KNNVectorInline]
    model = KNNClassifier

admin.site.register(Question, QuestionInline)
admin.site.register(Survey)
admin.site.register(Response, ResponseAdmin)
admin.site.register(TextAns)
admin.site.register(ChoiceAns)
admin.site.register(IntegerAns)
admin.site.register(BooleanAns)

admin.site.register(StudentQuestionSlider, StudentQuestionSliderAdmin)
admin.site.register(StudentQuestionGrading, StudentQuestionGradingAdmin)
admin.site.register(StudentAnswerSlider, AnswerSliderAdmin)
admin.site.register(StudentAnswerGrading, AnswerGradingAdmin)

admin.site.register(WorkField, WorkFieldAdmin)
admin.site.register(WorkFieldArea, WorkFieldAreaAdmin)
admin.site.register(StudentAnswerWorkField)

admin.site.register(SwedenRegion, SwedenRegionAdmin)
admin.site.register(Continent, ContinentAdmin)
admin.site.register(SwedenCity, SwedenCityAdmin)
admin.site.register(StudentAnswerContinent, StudentAnswerContinentAdmin)
admin.site.register(StudentAnswerRegion, StudentAnswerRegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(JobType, JobTypeAdmin)
admin.site.register(StudentAnswerJobType, StudentAnswerJobTypeAdmin)

admin.site.register(KNNClassifier, KNNClassifierAdmin)
