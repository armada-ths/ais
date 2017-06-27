from django.contrib import admin
from .models import Answer, ChoiceAns, TextAns, BooleanAns, Question

admin.site.register(Answer)
admin.site.register(ChoiceAns)
admin.site.register(TextAns)
admin.site.register(BooleanAns)
admin.site.register(Question)
