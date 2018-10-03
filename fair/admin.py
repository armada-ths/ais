from django.contrib import admin
from .models import Fair, Partner, Tag, OrganizationGroup

admin.site.register(Fair)
admin.site.register(Partner)
admin.site.register(Tag)
admin.site.register(OrganizationGroup)
