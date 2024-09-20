from django.contrib import admin
from .models import Language, Programme, Profile, DietaryRestriction
from improved_admin import ModelAdminImproved

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
class ProfileAdmin(ModelAdminImproved):
    search_fields = (
        "user__first_name",
        "user__last_name",
    )


@admin.register(Language)
class LanguageAdmin(ModelAdminImproved):
    pass


@admin.register(Programme)
class ProgrammeAdmin(ModelAdminImproved):
    pass


@admin.register(DietaryRestriction)
class DietaryRestrictionAdmin(ModelAdminImproved):
    pass
