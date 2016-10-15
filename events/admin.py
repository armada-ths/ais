from django.contrib import admin
from .models import Event, EventAttendence, EventQuestion, EventAnswer


class QuestionInline(admin.StackedInline):
    model = EventQuestion
    extra = 0


class EventAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    filter_horizontal = ("allowed_groups",)


class AnswerInline(admin.StackedInline):
    model = EventAnswer


class EventAttendenceAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Event, EventAdmin)

admin.site.register(EventAttendence, EventAttendenceAdmin)
