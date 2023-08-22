from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.db import models
import django.forms as forms

#Own subclass of ModelAdmin to override appearances of forms on admin panel.
class ModelAdminImproved(admin.ModelAdmin):

    def __init__(self, model: type, admin_site: AdminSite | None) -> None:
        super().__init__(model, admin_site)
        
    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple()},
    }