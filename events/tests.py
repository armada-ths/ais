from datetime import datetime
from django.test import TestCase
from events.models import Event
from fair.models import Fair


class EventsTestCase(TestCase):
    def setUp(self):
        fair = Fair.objects.create()

        Event.objects.create(
            name="Test event",
            fair=fair,
            date_start=datetime.now(),
            date_end=datetime.now(),
            signup_cr=False,
            signup_s=True,
            teams_create_cr=False,
            teams_create_s=True,
            teams_participate_cr=False,
            teams_participate_s=True,
            published=False,
        )

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        event = Event.objects.get(name="Test event")
        self.assertEqual(event.name, "Test event")
        self.assertEqual(event.signup_cr, False)
