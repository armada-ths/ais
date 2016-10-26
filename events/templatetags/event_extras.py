from django import template
from events.models import EventAttendence
from lib.util import before, after, has_common_element

register = template.Library()


@register.filter(name='user_eligible_event')
def user_eligible_event(user, event):
    if event.public_registration:
        return True
    return has_common_element(
        user.groups.all(), event.allowed_groups.all())


@register.filter(name='user_attending_event')
def user_attending_event(user, event):
    return EventAttendence.objects.filter(
        user=user.id, event=event.id).exists()


@register.filter(name='user_accepted_event')
def user_accepted_event(user, event):
    ea = EventAttendence.objects.filter(user=user.id, event=event.id)[0]
    return ea.status == 'A'


@register.filter(name='user_declined_event')
def user_declined_event(user, event):
    ea = EventAttendence.objects.filter(user=user.id, event=event.id)[0]
    return ea.status == 'D'


@register.filter(name='user_pending_event')
def user_pending_event(user, event):
    ea = EventAttendence.objects.filter(user=user.id, event=event.id)[0]
    return ea.status == 'S'


@register.filter(name='registration_open')
def registration_open(event):
    return after(event.registration_start) and before(event.registration_end)


@register.filter(name='registration_not_started')
def registration_not_started(event):
    return before(event.registration_start)


@register.filter(name='registration_closed')
def registration_closed(event):
    return after(event.registration_end)


@register.filter(name='registration_required')
def registration_required(event):
    return event.registration_required
