from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.db import models
import django.forms as forms
from recruitment.models import ExtraField

EXCLUDED_FIELDS = [ExtraField]

from datetime import date
from django.utils.translation import gettext_lazy as _


# This filter exposes all years in descending order, with
# the newest year at the top
class SortedFairYear(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("Fair year")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "fair"

    def lookups(self, request, model_admin):
        # Query to get distinct fairs ordered by year
        queryset = (
            model_admin.model.objects.select_related("fair")
            .order_by("-fair__year")
            .distinct("fair__year", "fair")
        )

        # Creating a list of tuples in the format (fair_id, fair.year)
        return [(obj.fair.id, obj.fair.year) for obj in queryset]

    def queryset(self, request, queryset):
        # Only fetches the fields related to the selected fair year
        if self.value():
            queryset = queryset.filter(fair__id=self.value())
        return queryset


# Own subclass of ModelAdmin to override appearances of forms on admin panel.
class ModelAdminImproved(admin.ModelAdmin):
    # Default search field, will need to be overridden for models without a name field
    search_fields = ("name",)

    def __init__(self, model, admin_site: AdminSite | None):
        super().__init__(model, admin_site)

    # Overrides get_autocomplete_fields to be all foreignkey fields.
    def get_autocomplete_fields(self, request):
        autocomplete_fields = []

        for field in self.model._meta.fields:
            if isinstance(field, (models.ForeignKey)):
                if field.related_model not in EXCLUDED_FIELDS:
                    autocomplete_fields.append(field.name)

        return autocomplete_fields

    formfield_overrides = {
        models.ManyToManyField: {"widget": forms.CheckboxSelectMultiple()},
    }
