from datetime import datetime
from django.contrib import admin

from django.http import HttpResponse
from .models import SignupContract, SignupLog
from django.utils.translation import gettext_lazy as _


class SignupLogDescendingFilter(admin.SimpleListFilter):
    title = _("Year")
    parameter_name = "contract__fair__year"

    def lookups(self, request, model_admin):
        # Retrieve all unique years from the related model and sort them in descending order
        years = (
            model_admin.model.objects.order_by("-contract__fair__year")
            .values_list("contract__fair__year", flat=True)
            .distinct()
        )
        return [(year, year) for year in years]

    # Default to current year selected
    def value(self):
        # Default to the current year if no specific value is selected
        if not self.used_parameters.get(self.parameter_name):
            return str(datetime.now().year)
        return super().value()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(contract__fair__year=self.value())
        return queryset


# Overrides admin register to add custom actions
@admin.register(SignupLog)
class SignupLogAdmin(admin.ModelAdmin):
    search_fields = ["company__name"]
    ordering = ["-timestamp"]
    list_display = ["company", "contract", "timestamp", "type"]
    list_filter = ["type", SignupLogDescendingFilter]


class SignupContractDescendingFilter(admin.SimpleListFilter):
    title = _("Year")
    parameter_name = "fair__year"

    def lookups(self, request, model_admin):
        # Retrieve all unique years from the related model and sort them in descending order
        years = (
            model_admin.model.objects.order_by("-fair__year")
            .values_list("fair__year", flat=True)
            .distinct()
        )
        return [(year, year) for year in years]

    # Default to current year selected
    def value(self):
        # Default to the current year if no specific value is selected
        if not self.used_parameters.get(self.parameter_name):
            return str(datetime.now().year)
        return super().value()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(fair__year=self.value())
        return queryset


@admin.register(SignupContract)
class SignupContractAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "is_timely",
        "current",
        "default",
    )
    list_filter = ["type", SignupContractDescendingFilter]
