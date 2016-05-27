from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.contrib import admin
from .models import Profile

class ProfileInline(admin.StackedInline):
	model = Profile
	fk_name = 'user'
	max_num = 1
	verbose_name_plural = "Profile"

class CustomUserAdmin(UserAdmin):
	inlines = [ProfileInline,]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

