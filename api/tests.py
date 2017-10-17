from django.contrib.auth.models import User, Group
from django.http.response import Http404
from django.test import TestCase, RequestFactory, Client
from django.utils import timezone

import json, datetime

from banquet.models import BanquetteAttendant
from companies.models import Company
from events.models import Event
from exhibitors.models import Exhibitor, CatalogInfo
from fair.models import Fair
from matching.models import StudentQuestionType, StudentQuestionSlider, WorkField, WorkFieldArea, Survey
from recruitment.models import RecruitmentPeriod, Role
from student_profiles.models import StudentProfile

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

class Organization(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        fair = Fair.objects.create(name='Current Fair', current=True)
        group1 = Group.objects.create(name='Group1')
        group2 = Group.objects.create(name='Group2')
        role1 = Role.objects.create(name='Role1', group=group1)
        role2 = Role.objects.create(name='Role2', group=group2)
        recruitment = RecruitmentPeriod.objects.create(
            name="recruitment period",
            fair=fair,
            start_date=timezone.now(),
            end_date=timezone.now(),
            interview_end_date=timezone.now())
        recruitment.recruitable_roles.set([role1, role2])
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2', first_name='first', last_name='last')
        user3 = User.objects.create(username='user3')
        programme = Programme.objects.create(name='Programme')
        profile1 = Profile.objects.create(user=user1, linkedin_url='url.url.se', programme=programme)
        profile2 = Profile.objects.create(user=user2, linkedin_url='url.url.se', picture_original='picture.original.url')
        profile1.user = user1
        profile1.save()
        profile2.user=user2
        profile2.save() 
        user1.groups.set([group1])
        user2.groups.set([group2])
        user3.groups.set([group1])

    def test_view(self):
        request = self.factory.get('/api/organization', HTTP_HOST='host')
        response = views.organization(request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        organization = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(organization), 2)
        self.assertEqual(organization[0]['role'], 'Group1')
        self.assertEqual(len(organization[0]['people']), 2)
        self.assertEqual(len(organization[1]['people']), 1)
        self.assertEqual(organization[1]['people'][0]['role'], 'Group2')
        self.assertEqual(len(organization[1]['people'][0]), 6)
        self.assertEqual(len(organization[0]['people'][1]), 3)
        self.assertEqual(organization[1]['people'][0]['picture'], 'http://host/media/picture.original.url')
        self.assertEqual(organization[0]['people'][0]['picture'], 'http://host/static/images/no-image.png')
        self.assertEqual(organization[0]['people'][0]['programme'], 'Programme')

class QuestionsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        (self.fair, wasCreated) = Fair.objects.get_or_create(name='Armada fair', current=True)
        (self.survey, wasCreated) = Survey.objects.get_or_create(name='Dummy survey', fair=self.fair)

        # generate questions
        questions = [
            StudentQuestionSlider.objects.create(question='Question 1?',
                min_value=0.0, max_value=10000.0, step=0.1),

            StudentQuestionSlider.objects.create(question='Some other question?',
            min_value=0.0, max_value=1000000.0, step=1.0)
        ]
        for question in questions:
            question.save()
            question.survey.add(self.survey)

        # generate areas
        (work_area, wasCreated) = WorkFieldArea.objects.get_or_create(work_area='Test area')
        fields = [
            WorkField.objects.get_or_create(work_area=work_area, work_field='Test field'),
            WorkField.objects.get_or_create(work_area=work_area, work_field='Another field')
        ]
        for (field, wasCreated) in fields:
            if wasCreated:
                field.save()
                field.survey.add(self.survey)


    def test_get(self):
        # make a request
        request = self.factory.get('/api/questions')
        response = views.questions(request)

        # validate the response
        data = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(data), 2)

        # validate questions
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(data['questions'][0]['question'], 'Question 1?')
        self.assertEqual(data['questions'][1]['step'], 1.0)

        #validate areas
        self.assertEqual(len(data['areas']), 1)
        self.assertEqual(len(data['areas'][0]), 2)
        self.assertEqual(len(data['areas'][0]['fields']), 2)
        self.assertEqual(data['areas'][0]['title'], 'Test area')
        self.assertEqual(data['areas'][0]['fields'][0], 'Test field')

        
class BanquetPlacementTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        current_fair = Fair.objects.create(name='Current fair', current=True)
        last_fair = Fair.objects.create(name='Last fair')
        company = Company.objects.create(name='Company')
        exhibitor = Exhibitor.objects.create(fair=current_fair, company=company)
        user = User.objects.create(username='user', password='password')
        banquette_attendant1 = BanquetteAttendant.objects.create(first_name='Nr1', user=user, fair=current_fair)
        banquette_attendant2 = BanquetteAttendant.objects.create(first_name='Nr2', exhibitor=exhibitor, fair=current_fair)
        banquette_attendant_last = BanquetteAttendant.objects.create(first_name='Last', user=user, fair=last_fair)

    def test_view(self):
        request = self.factory.get('/api/banquet_placement')
        response = views.banquet_placement(request)
        banquet_placement = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(banquet_placement), 2)
        self.assertEqual(banquet_placement[1]['first_name'],'Nr2')


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
