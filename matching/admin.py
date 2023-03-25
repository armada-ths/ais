from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import (
    Question,
    Answer,
    Category,
    Survey,
    Response,
    TextAns,
    ChoiceAns,
    IntegerAns,
    BooleanAns,
    StudentQuestionSlider,
    StudentQuestionGrading,
    StudentAnswerSlider,
    StudentAnswerGrading,
    WorkFieldArea,
    WorkField,
    StudentAnswerWorkField,
    SwedenRegion,
    Continent,
    StudentAnswerRegion,
    StudentAnswerContinent,
    SwedenCity,
    Country,
    JobType,
    StudentAnswerJobType,
)


class QuestionInline(admin.ModelAdmin):
    list_display = ("text", "question_type")


class AnswerInline(admin.StackedInline):
    fields = ("question", "ans")


class TextAnsInline(AnswerInline):
    model = TextAns


class ChoiceAnsInline(AnswerInline):
    model = ChoiceAns


class IntegerAnsInline(AnswerInline):
    model = IntegerAns


class BooleanAnsInline(AnswerInline):
    model = BooleanAns


class WorkFieldInline(admin.TabularInline):
    model = WorkField


class WorkFieldAreaAdmin(admin.ModelAdmin):
    list_display = ("work_area",)
    inlines = [WorkFieldInline]


class StudentAnswerWFieldInline(admin.TabularInline):
    list_display = ("student", "work_field", "answer")
    model = StudentAnswerWorkField


class WorkFieldAdmin(admin.ModelAdmin):
    list_display = ("work_field", "work_area")
    inlines = [StudentAnswerWFieldInline]


class AnswerSliderAdmin(admin.ModelAdmin):
    list_display = ("student", "question", "answer_min", "answer_max")
    model = StudentAnswerSlider


class AnswerGradingAdmin(admin.ModelAdmin):
    list_display = ("student", "question", "answer")
    model = StudentAnswerGrading


# Student Questions
class StudentQuestionSliderAdmin(admin.ModelAdmin):
    exclude = ("question_type",)
    model = StudentQuestionSlider


class StudentQuestionGradingAdmin(admin.ModelAdmin):
    exclude = ("question_type",)
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


class QuestionInline(admin.TabularInline):
    model = Question
    ordering = (
        "id",
        "category",
    )
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


class SurveyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("fair",)
    inlines = [CategoryInline, QuestionInline]


class ResponseAdmin(admin.ModelAdmin):
    list_display = ("survey", "exhibitor")
    list_filter = ("survey", "exhibitor")
    inlines = [TextAnsInline, ChoiceAnsInline, IntegerAnsInline, BooleanAnsInline]
    # specifies the order as well as which fields to act on
    readonly_fields = ("survey", "exhibitor")


# admin.site.register(Question, QuestionInline)
# admin.site.register(Category, CategoryInline)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)

admin.site.register(Answer)
# admin.site.register(Question, QuestionInline)
# admin.site.register(TextAns)
# admin.site.register(ChoiceAns)
# admin.site.register(IntegerAns)
# admin.site.register(BooleanAns)

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
