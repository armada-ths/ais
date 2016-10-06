from django.test import TestCase, RequestFactory
import json
from django.utils import timezone

from fair.models import Fair
from companies.models import Company
from events.models import Event
from .serializers import company_serializer, event_serializer
from . import views

HTTP_status_code_OK = 200

class ExhibitorTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.company = Company.objects.create(name='test')

    def test_company_serializer(self):
        serialized = company_serializer(self.company)
        self.assertIn('id', serialized)
        self.assertIn('name', serialized)

    def test_view(self):
        request = self.factory.get('/api/exhibitors/')
        response = views.exhibitors(request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        companies = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(companies), 1)
        self.assertEqual(companies[0]['id'], self.company.pk)

class EventTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        now = timezone.now()
        Fair.objects.create(name="Armada 2000")
        test_fair = Fair.objects.get(name="Armada 2000")
        self.event = Event.objects.create(fair=test_fair, name='test', event_start=now, event_end=now, registration_start=now, registration_end=now, registration_last_day_cancel=now, public_registration=True)
        self.hidden_event = Event.objects.create(fair=test_fair, name='hidden event', event_start=now, event_end=now, registration_start=now, registration_end=now, registration_last_day_cancel=now, public_registration=False)

    def test_event_serializer(self):
        data = event_serializer(self.event)
        self.assertIn('id', data)
        self.assertIn('name', data)

    def test_view(self):
        request = self.factory.get('/api/events/')
        response = views.events(request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        events = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['id'], self.event.pk)

class NewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_view(self):
        request = self.factory.get('/api/news/')
        response = views.news(request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        news = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(news), 0)
