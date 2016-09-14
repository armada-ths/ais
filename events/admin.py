from django.contrib import admin
from .models import Event, EventAttendence, EventQuestion, EventAnswer

class QuestionInline(admin.StackedInline):
    model = EventQuestion
    extra = 3


class EventAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Event, EventAdmin)
admin.site.register(EventAttendence)
admin.site.register(EventAnswer)
