from django import template
from events.models import EventAttendence

register = template.Library()

@register.filter(name='user_attending_event')
def user_attending_event(user, event):
    return EventAttendence.objects.filter(user=user.id, event=event.id).exists()
