from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.db import models
import django.forms as forms

#Own subclass of ModelAdmin to override appearances of forms on admin panel.
class ModelAdminImproved(admin.ModelAdmin):

    def __init__(self, model, admin_site: AdminSite | None):
        super().__init__(model, admin_site)
        self.search_fields = ['name'] #Default search field
        
    #Overrides get_autocomplete_fields to be all foreignkey and manytomany fields.
    def get_autocomplete_fields(self, request):
        autocomplete_fields = []
        for field in self.model._meta.fields:
            if isinstance(field, (models.ForeignKey, models.ManyToManyField)):
                autocomplete_fields.append(field.name)
        return autocomplete_fields
    
    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple()},
    }