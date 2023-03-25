from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.contrib import admin
from .models import Language, Programme, Profile, DietaryRestriction

"""
class ProfileInline(admin.StackedInline):
	model = Profile
	fk_name = 'user'
	max_num = 1
	verbose_name_plural = "Profile"

class CustomUserAdmin(UserAdmin):
	inlines = [ProfileInline,]
	
	# We need double __ to search in foreign keys. We've added search
	# results from profile
	search_fields = ['first_name', 'last_name', 'email', 'profile__drivers_license', 'profile__phone_number', 'profile__programme',]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

"""


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = (
        "user__first_name",
        "user__last_name",
    )


admin.site.register(Language)
admin.site.register(Programme)
admin.site.register(DietaryRestriction)
