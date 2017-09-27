'''
Custom tags for template uses
'''

from django import template

from exhibitors.models import Exhibitor

register = template.Library()

def field_hosts(model):
    retstr = ''
    for host in model.hosts.all():
        retstr += host.get_full_name() + '\n'
    return retstr


def field_superiors(model):
    retstr = ''
    for superior in model.superiors():
        retstr += superior.get_full_name() + '\n'
    return retstr


special_fields = {
    'hosts': field_hosts,
    'superiors': field_superiors
}


# Filters are used like {{ item|filter:arg }}
@register.filter(name='get_value')
def getFieldValue(model, field):
    if field in special_fields:
        special_field_model = model
        return special_fields[field](model)
    elif hasattr(model._meta.get_field(field), 'choices') and model._meta.get_field(field).choices:
        field = 'get_' + field + '_display' # getattr(model, field) will be able to call the method
        if hasattr(model, str(field)):
            return getattr(model, field)()
    elif hasattr(model, str(field)):
        return getattr(model, field)
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
