from django import template

from exhibitors.models import ExhibitorView

register = template.Library()


# Filters are used like {{ item|filter:arg }}
@register.filter(name="get_value")
def getFieldValue(model, field):
    if (
        hasattr(model._meta.get_field(field), "choices")
        and model._meta.get_field(field).choices
    ):
        field = (
            "get_" + field + "_display"
        )  # getattr(model, field) will be able to call the method
        if hasattr(model, str(field)):
            return getattr(model, field)()

    elif hasattr(model, str(field)):
        return getattr(model, field)

    return "Unknown value"


# Tags are used like {% tag arg %}
@register.simple_tag(name="get_field_name")
def getFieldName(name):
    return ExhibitorView.selectable_fields[name]
