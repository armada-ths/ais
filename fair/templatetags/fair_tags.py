from django import template
from fair.models import Fair

register = template.Library()

@register.filter(name='is_armada_member')
def is_armada_member(user):
	return Fair.objects.get(name='Armada 2016').is_member_of_fair(user)
