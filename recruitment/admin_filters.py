from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class SortedRecruitmentPeriod(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("Recruitment period")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "recruitment_period"

    def lookups(self, request, model_admin):
        # Query to get distinct fairs ordered by year
        queryset = model_admin.model.objects.select_related(
            "recruitment_period", "recruitment_period__fair"
        ).order_by("-recruitment_period__fair__year", "recruitment_period")

        # Remove duplicates
        raw = [value for value in queryset]
        included_recruitment_periods = dict()
        result = []
        for i in range(len(raw)):
            if raw[i].recruitment_period not in included_recruitment_periods:
                included_recruitment_periods[raw[i].recruitment_period] = True
                result.append(raw[i])

        # Creating a list of tuples in the format (fair_id, fair.year)
        return [(obj.recruitment_period.id, obj.recruitment_period) for obj in result]

    def queryset(self, request, queryset):
        # Only fetches the fields related to the selected fair year
        if self.value() is not None:
            queryset = queryset.filter(recruitment_period__id=self.value())
        return queryset
