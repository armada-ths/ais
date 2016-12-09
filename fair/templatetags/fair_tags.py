from django import template
from fair.models import Fair

register = template.Library()

@register.filter(name='is_armada_member')
def is_armada_member(user):
    # This should not be hard coded
    fair = Fair.objects.latest('id')
    if fair is not None:
        return fair.is_member_of_fair(user)
    return False
