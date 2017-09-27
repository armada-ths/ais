from django.test import TestCase, RequestFactory
import json
from django.utils import timezone

from fair.models import Fair
from companies.models import Company
from exhibitors.models import Exhibitor, CatalogInfo
from events.models import Event
import api.serializers as serializers
from . import views

HTTP_status_code_OK = 200


class ExhibitorTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory(HTTP_HOST='test.com')
        company = Company.objects.create(name='test')
        fair = Fair.objects.create(name='Armada 2016', current=True, year=2016)
        self.exhibitor = Exhibitor.objects.create(
                company=company,
                fair=fair,
                wants_information_about_events=False,
                wants_information_about_targeted_marketing=False,
                wants_information_about_osqledaren=False,
                )
        self.cataloginfo = CatalogInfo(
                exhibitor=self.exhibitor,
                display_name='test test',
                )
        self.cataloginfo.save()
        self.request = self.factory.get('/api/exhibitors/')

    def test_serializer(self):
        serialized = serializers.exhibitor(
                self.request,
                self.exhibitor.cataloginfo
                )
        self.assertIn('id', serialized)
        self.assertIn('name', serialized)

    def test_view(self):
        response = views.exhibitors(self.request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        exhibitors = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(exhibitors), 1)
        self.assertEqual(exhibitors[0]['id'], self.cataloginfo.pk)


class EventTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory(HTTP_HOST='test.com')

        now = timezone.now()
        test_fair = Fair(name="Armada 2000", current=False, year=2000)
        test_fair.save()

        self.event = Event(
            fair=test_fair, name='test', event_start=now, event_end=now,
            registration_start=now, registration_end=now,
            registration_last_day_cancel=now, public_registration=True, published=True)
        self.event.save()
        self.hidden_event = Event(
            fair=test_fair, name='hidden event', event_start=now,
            event_end=now, registration_start=now, registration_end=now,
            registration_last_day_cancel=now, public_registration=False)
        self.hidden_event.save()
        self.request = self.factory.get('/api/events/')

    def test_event_serializer(self):
        data = serializers.event(self.request, self.event)
        self.assertIn('id', data)
        self.assertIn('name', data)

    def test_view(self):
        response = views.events(self.request)
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
