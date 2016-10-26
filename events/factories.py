import factory
from django.utils import timezone

from fair.factories import FairFactory
from .models import Event


class EventFactory(factory.DjangoModelFactory):
    fair = factory.SubFactory(FairFactory)
    name = "Armada 1993"
    event_start = timezone.now()
    event_end = timezone.now()
    registration_open = timezone.now()
    registration_last_day = timezone.now()
    registration_last_day_cancel = timezone.now()
    public_registration = True

    class Meta:
        model = Event


class HiddenEventFactory(factory.DjangoModelFactory):
    fair = factory.SubFactory(FairFactory)
    name = "Hidden Event"
    event_start = timezone.now()
    event_end = timezone.now()
    registration_open = timezone.now()
    registration_last_day = timezone.now()
    registration_last_day_cancel = timezone.now()
    public_registration = False

    class Meta:
        model = Event
