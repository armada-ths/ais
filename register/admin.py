from django.contrib import admin

from .models import SignupContract, SignupLog
# Register your models here.
admin.site.register(SignupContract)
admin.site.register(SignupLog)
