from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

UserAdmin.list_display = ('email', 'first_name', 'last_name', 'is_staff', 'last_login')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
