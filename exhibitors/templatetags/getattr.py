'''
Custom tags for template uses
'''

from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='getattr')
def getattribute(value, arg):
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    else:
        return settings.TEMPLATE_STRING_IF_INVALID
