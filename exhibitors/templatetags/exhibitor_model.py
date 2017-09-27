'''
Custom tags for template uses
'''

from django import template

from exhibitors.models import Exhibitor

register = template.Library()

# Filters are used like {{ item|filter:arg }}
@register.filter(name='get_value')
def getFieldValue(model, field):
    if hasattr(model, str(field)):
        return getattr(model, field)
    else:
        return ''   # it might be smarter to have a string in Settings for this


# A dictionary for table view, fields not present here will take their verbose name from Exhibitor model
names = {
    'banquetteattendant': 'Banquette attendant'
}

# Tags are used like {% tag arg %}
@register.simple_tag(name='get_field_name')
def getFieldName(name):
    if name in names:
        return names[name]
    else:
        return Exhibitor._meta.get_field(name).verbose_name.capitalize()
