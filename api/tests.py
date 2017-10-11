from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.http.response import Http404
import datetime

import json

from fair.models import Fair
from companies.models import Company
from exhibitors.models import Exhibitor, CatalogInfo
from events.models import Event
from student_profiles.models import StudentProfile

from recruitment.models import RecruitmentPeriod, Role
import api.serializers as serializers
from . import views

import api.serializers as serializers


HTTP_status_code_OK = 200
STUDENT_PROFILE_SIZE = 1


class ExhibitorTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory(HTTP_HOST='test.com')
        self.company = Company.objects.create(name='test')
        fair = Fair.objects.create(name='Armada 2016', current=True)
        self.exhibitor = Exhibitor.objects.create(
                company=self.company,
                fair=fair,
                )
        self.request = self.factory.get('/api/exhibitors')


    def test_serializer(self):
        serialized = serializers.exhibitor(
                self.request,
                self.exhibitor,
                self.exhibitor.company
                )
        self.assertIn('company', serialized)


    def test_view(self):
        response = views.exhibitors(self.request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        exhibitors = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(exhibitors), 1)
        self.assertEqual(exhibitors[0]['fair'], self.exhibitor.fair.name)
        self.assertEqual(exhibitors[0]['company'], self.company.name)


class EventTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory(HTTP_HOST='test.com')

        now = timezone.now()
        test_fair = Fair(name="Armada 2000", current=True)
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


class StudentProfileTestCase(TestCase):
    def check_student_profile_response(self, response, expected_nickname = None):
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        profile = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(profile), STUDENT_PROFILE_SIZE)
        if expected_nickname:
            self.assertEqual(profile['nickname'], expected_nickname)


    def setUp(self):
        self.factory = RequestFactory()
        self.url_prefix = '/api/student_profile'
        StudentProfile.objects.get_or_create(pk=1, nickname='Pre_post')
        StudentProfile.objects.get_or_create(pk=2, nickname='Unmodified')
        

    # Test that this api works without a login
    def test_client(self):
        client = Client()
        
        response = client.get(self.url_prefix + '?student_id=1')
        self.check_student_profile_response(response, 'Pre_post')
        
        response = client.put(self.url_prefix + '?student_id=1',
            data = json.dumps({'nickname' : 'Postman'}))
        self.check_student_profile_response(response, 'Postman')


    # Test the PUT protocol
    def test_put(self):
        request = self.factory.put(self.url_prefix + '?student_id=1',
            data = json.dumps({'nickname' : 'Postman'}))
        response = views.student_profile(request)

        self.check_student_profile_response(response, 'Postman')

        self.assertFalse(StudentProfile.objects.filter(pk=3).first())
        
        request = self.factory.put(self.url_prefix + '?student_id=3',
            data=json.dumps({'nickname' : 'Mojo'}))
        response = views.student_profile(request)

        self.check_student_profile_response(response, 'Mojo')

        self.assertTrue(StudentProfile.objects.filter(pk=3).first())
        self.assertEqual(StudentProfile.objects.get(pk=1).nickname, 'Postman')
        self.assertEqual(StudentProfile.objects.get(pk=2).nickname, 'Unmodified')
        self.assertEqual(StudentProfile.objects.get(pk=3).nickname, 'Mojo')

    
    # Test the GET protocol
    def test_get(self):
        request = self.factory.get(self.url_prefix + '?student_id=1')
        response = views.student_profile(request)
        
        self.check_student_profile_response(response, 'Pre_post')
        
        request = self.factory.get(self.url_prefix + '?student_id=0')
        try:
            response = views.student_profile(request)
        except Http404:
            pass    # we expect a 404 as the student with pk=0 doesn't exist!


class RecruitmentTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        fair = Fair(name='Armada 2017', current=True)
        fair.save()
        tomorrow = timezone.now() + datetime.timedelta(days=1)
        yesterday = timezone.now() - datetime.timedelta(days=1)
        role=Role(name="Role")
        recruitment = RecruitmentPeriod(
            name="current recruitment", 
            start_date=yesterday, 
            end_date=tomorrow, 
            interview_end_date=tomorrow, 
            fair=fair,
        )
        recruitment.save()
        recruitment2 = RecruitmentPeriod(
            name="current recruitment2", 
            start_date=yesterday, 
            end_date=tomorrow, 
            interview_end_date=tomorrow, 
            fair=fair,
        )
        recruitment2.save()
        recruitment_past = RecruitmentPeriod(
            name="past recruitment", 
            start_date=yesterday, 
            end_date=yesterday, 
            interview_end_date=tomorrow, 
            fair=fair,
        )
        recruitment_past.save()
        recruitment_future = RecruitmentPeriod(
            name="past recruitment", 
            start_date=tomorrow, 
            end_date=tomorrow, 
            interview_end_date=tomorrow, 
            fair=fair,
        )
        recruitment_future.save()
    def test_view(self):
        #See that all current recruitment are included but not recruitments that are not open
        request = self.factory.get('/api/recruitment')
        response = views.recruitment(request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        recruitments = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(recruitments), 2)
        #Test content for one recruitment
        self.assertEqual(recruitments[0]['name'], 'current recruitment')
