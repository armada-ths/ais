from django.contrib import admin
from .models import StudentProfile, MatchingResult

# Register your models here.

admin.site.register(StudentProfile)
admin.site.register(MatchingResult)
