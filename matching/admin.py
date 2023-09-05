from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from improved_admin import ModelAdminImproved

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


class QuestionInline(ModelAdminImproved):
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


class WorkFieldAreaAdmin(ModelAdminImproved):
    list_display = ("work_area",)
    inlines = [WorkFieldInline]


class StudentAnswerWFieldInline(admin.TabularInline):
    list_display = ("student", "work_field", "answer")
    model = StudentAnswerWorkField


class WorkFieldAdmin(ModelAdminImproved):
    list_display = ("work_field", "work_area")
    inlines = [StudentAnswerWFieldInline]


class AnswerSliderAdmin(ModelAdminImproved):
    list_display = ("student", "question", "answer_min", "answer_max")
    model = StudentAnswerSlider


class AnswerGradingAdmin(ModelAdminImproved):
    list_display = ("student", "question", "answer")
    model = StudentAnswerGrading


# Student Questions
class StudentQuestionSliderAdmin(ModelAdminImproved):
    exclude = ("question_type",)
    model = StudentQuestionSlider


class StudentQuestionGradingAdmin(ModelAdminImproved):
    exclude = ("question_type",)
    model = StudentQuestionGrading


class SwedenRegionAdmin(ModelAdminImproved):
    model = SwedenRegion


class ContinentAdmin(ModelAdminImproved):
    model = Continent


class SwedenCityAdmin(ModelAdminImproved):
    model = SwedenCity


class StudentAnswerContinentAdmin(ModelAdminImproved):
    model = StudentAnswerContinent


class StudentAnswerRegionAdmin(ModelAdminImproved):
    model = StudentAnswerRegion


class CountryAdmin(ModelAdminImproved):
    model = Country


class JobTypeAdmin(ModelAdminImproved):
    model = JobType


class StudentAnswerJobTypeAdmin(ModelAdminImproved):
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


class SurveyAdmin(ModelAdminImproved):
    list_display = ("name",)
    list_filter = ("fair",)
    inlines = [CategoryInline, QuestionInline]


class ResponseAdmin(ModelAdminImproved):
    list_display = ("survey", "exhibitor")
    list_filter = ("survey", "exhibitor")
    inlines = [TextAnsInline, ChoiceAnsInline, IntegerAnsInline, BooleanAnsInline]
    # specifies the order as well as which fields to act on
    readonly_fields = ("survey", "exhibitor")


# admin.site.register(Question, QuestionInline)
# admin.site.register(Category, CategoryInline)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)


@admin.register(Answer)
class AnswerAdmin(ModelAdminImproved):
    pass


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
