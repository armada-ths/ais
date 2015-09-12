from django.test import TestCase
from django.core.urlresolvers import reverse
from events.models import Event
from events.forms import EventAttendenceForm,EventForm

class EventTest(TestCase):

    # Create simple event object
    # @return Event object
    def create_event(self, name="ABC", capacity=1337, description="Awesome event"):
        return Event.objects.create(name=name,capacity=capacity,description=description)

    # Testing if names are
    def test_created_event(self):
        e = self.create_event()
        self.assertTrue(isinstance(e,Event))
        self.assertEqual(e.__unicode__(), e.name)
        self.assertEqual(1337, e.capacity)
        self.assertEqual("Awesome event", e.description)
        self.assertIsNot("Freckin awesome event", e.description)

    def test_valid_event_form(self):
        e = Event.objects.create(name="ABC",capacity=1337,description="Just awesome")
        data = {"name":e.name, "capacity":e.capacity,"description":e.description}
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())
