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

from student_profiles.models import StudentProfile, MatchingResult
from matching.models import StudentQuestionType, StudentQuestionSlider, StudentQuestionGrading, StudentQuestionBase, \
WorkField, WorkFieldArea, Survey, StudentAnswerBase, StudentAnswerSlider, StudentAnswerGrading, StudentAnswerWorkField, \
StudentAnswerJobType, StudentAnswerRegion, JobType, Region
from people.models import Profile, Programme
from recruitment.models import RecruitmentPeriod, Role

from . import views

import api.serializers as serializers


HTTP_status_code_OK = 200
STUDENT_PROFILE_SIZE = 4


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
    '''
    Test both PUT and GET requests for Student profile.
    ais.armada.nu/api/student_profile?student_id={STUDENT_ID}
    '''
    def check_student_profile(self, profile, nickname = None, linkedin = None, facebook = None, phone_number = None):
        student = StudentProfile.objects.filter(pk=profile).first()
        self.assertTrue(student)

        if nickname:
            self.assertEqual(student.nickname, nickname)
        if linkedin:
            self.assertEqual(student.linkedin_profile, linkedin)
        if facebook:
            self.assertEqual(student.facebook_profile, facebook)
        if phone_number:
            self.assertEqual(student.phone_number, phone_number)


    def check_response(self, response, nickname=None, linkedin=None, facebook=None, phone_number=None):
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        data = json.loads(response.content.decode(response.charset))
        self.assertTrue(type(data) is dict)

        if nickname:
            self.assertEqual(data['nickname'], nickname)
        if linkedin:
            self.assertEqual(data['linkedin_profile'], linkedin)
        if facebook:
            self.assertEqual(data['facebook_profile'], facebook)
        if phone_number:
            self.assertEqual(data['phone_number'], phone_number)


    def setUp(self):
        self.factory = RequestFactory()
        self.url_prefix = '/api/student_profile'
        StudentProfile.objects.get_or_create(pk=1, nickname='Pre_post')
        StudentProfile.objects.get_or_create(pk=2, nickname='Unmodified')
        StudentProfile.objects.get_or_create(pk=32, nickname='Full', linkedin_profile='linkedin', facebook_profile='facebook', phone_number='911')


    # Test that this api works without a login
    def test_client(self):
        client = Client()
        
        response = client.get(self.url_prefix + '?student_id=1')
        self.check_response(response, 'Pre_post')
        
        response = client.put(self.url_prefix + '?student_id=1',
            data = json.dumps({'nickname' : 'Postman'}))
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        self.check_student_profile(1, 'Postman')


    # Test the PUT protocol
    def test_put(self):
        request = self.factory.put(self.url_prefix + '?student_id=1',
            data = json.dumps({'nickname' : 'Postman'}))
        response = views.student_profile(request)

        self.check_student_profile(1, 'Postman')

        self.assertFalse(StudentProfile.objects.filter(pk=3).first())
        
        request = self.factory.put(self.url_prefix + '?student_id=3',
            data=json.dumps({'nickname' : 'Mojo'}))
        response = views.student_profile(request)

        self.check_student_profile(3, 'Mojo')

        self.assertTrue(StudentProfile.objects.filter(pk=3).first())
        self.assertEqual(StudentProfile.objects.get(pk=1).nickname, 'Postman')
        self.assertEqual(StudentProfile.objects.get(pk=2).nickname, 'Unmodified')
        self.assertEqual(StudentProfile.objects.get(pk=3).nickname, 'Mojo')

        request = self.factory.put(self.url_prefix + '?student_id=12',
            data=json.dumps({
                'nickname' : 'Request',
                'facebook_profile' : 'face',
                'phone_number' : '05'}))
        response = views.student_profile(request)

        self.check_student_profile(12, 'Request', facebook='face', phone_number='05')

        request = self.factory.put(self.url_prefix + '?student_id=49',
            data=json.dumps(['bleh bleh']))
        response = views.student_profile(request)
        self.assertEqual(response.status_code, 406)

        request = self.factory.put(self.url_prefix + '?student_id=49',
            data=json.dumps({'noname' : 'name', 'phone_number':'12'}))
        self.assertEqual(response.status_code, 406)

        self.assertFalse(StudentProfile.objects.filter(pk=49).first())


    # Test the GET protocol
    def test_get(self):
        request = self.factory.get(self.url_prefix + '?student_id=1')
        response = views.student_profile(request)

        self.check_response(response, 'Pre_post')

        request = self.factory.get(self.url_prefix + '?student_id=0')
        try:
            response = views.student_profile(request)
        except Http404:
            pass    # we expect a 404 as the student with pk=0 doesn't exist!

        request = self.factory.get(self.url_prefix + '?student_id=32')
        response = views.student_profile(request)
        self.check_response(response, 'Full', 'linkedin', 'facebook', '911')


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
        self.questions = [
            StudentQuestionSlider.objects.create(question='Question 1?',
                min_value=0.0, max_value=10000.0),

            StudentQuestionSlider.objects.create(question='Some other question?',
                min_value=0.0, max_value=1000000.0, logarithmic=True, units='meters'),

            StudentQuestionGrading.objects.create(question='Wait what?',
                grading_size=5)
        ]
        for question in self.questions:
            question.save()
            question.survey.add(self.survey)

        # generate areas
        (work_area, wasCreated) = WorkFieldArea.objects.get_or_create(work_area='Test area')
        self.fields = [
            WorkField.objects.get_or_create(work_area=work_area, work_field='Test field'),
            WorkField.objects.get_or_create(work_area=work_area, work_field='Another field'),
            WorkField.objects.get_or_create(work_area=work_area, work_field='My field')
        ]
        for (field, wasCreated) in self.fields:
            if wasCreated:
                field.save()
                field.survey.add(self.survey)

        self.job_types = [
            JobType.objects.get_or_create(job_type='master thesis', job_type_id=1),
            JobType.objects.get_or_create(job_type='part time job', job_type_id=2)
        ]

        self.regions = [
            Region.objects.get_or_create(name='Africa', region_id=1),
            Region.objects.get_or_create(name='Asia' , region_id=2),
            Region.objects.get_or_create(name='Australia', region_id=3)
        ]

    def test_questions(self):
        # Make sure no questions share a PK
        # (they shouldn't, but if django changes its policies this test will catch it)
        questions = StudentQuestionBase.objects.all()
        ids = set()
        for question in questions:
            self.assertFalse(question.pk in ids)
            ids.add(question.pk)


    def test_get(self):
        # make a request
        request = self.factory.get('/api/questions')
        response = views.questions(request)

        # validate the response
        data = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(data), 2)

        # validate questions
        self.assertEqual(len(data['questions']), 3)
        for question in data['questions']:
            self.assertTrue('id' in question)
            self.assertTrue('type' in question)
            self.assertTrue('question' in question)
            self.assertTrue(StudentQuestionType.is_type(question['type']))
            if question['type'] == StudentQuestionType.SLIDER.value:
                self.assertTrue('min' in question)
                self.assertTrue('max' in question)
                self.assertTrue('logarithmic' in question)
                self.assertTrue('units' in question)
            elif question['type'] == StudentQuestionType.GRADING.value:
                self.assertTrue('count' in question)

        #validate areas
        self.assertEqual(len(data['areas']), 3)
        for area in data['areas']:
            self.assertTrue('id' in area)
            self.assertTrue('field' in area)
            self.assertTrue('area' in area)
            self.assertEqual(area['area'], 'Test area')


    def test_put(self):
        #create a paylioad:
        data = json.dumps({
            'questions' : [
                {'id' : self.questions[0].pk, 'answer' : {'min' : 2.0, 'max' : 3.0}},
                {'id' : self.questions[1].pk, 'answer' : {'min' : 1.0, 'max' : 15.0}},
                {'id' : self.questions[2].pk, 'answer' : -1}
            ], 'areas' : [
                self.fields[2][0].pk
            ], 'regions': [
                1
            ], 'continents': [
                2
            ],
            'looking_for': [
                1
            ]
        })
        request = self.factory.put('api/questions?student_id=2', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 200)

        def test_db():
            answers = StudentAnswerBase.objects.filter(student=StudentProfile.objects.get(pk=2))
            answer_list = []
            field_list = []
            region_list = []
            job_type_list = []

            for answer in answers:
                if hasattr(answer, 'studentanswerslider'):
                    answer_list.append(answer.studentanswerslider)
                elif hasattr(answer, 'studentanswergrading'):
                    answer_list.append(answer.studentanswergrading)
                elif hasattr(answer, 'studentanswerworkfield'):
                    field_list.append(answer.studentanswerworkfield)
                elif hasattr(answer, 'studentanswerregion'):
                    region_list.append(answer.studentanswerregion)
                elif hasattr(answer, 'studentanswerjobtype'):
                    job_type_list.append(answer.studentanswerjobtype)
                else:
                    self.assertFalse('Answer is not a subtype!')
            self.assertEqual(answer_list[0].question, self.questions[0])
            self.assertEqual(answer_list[1].question, self.questions[1])
            self.assertEqual(answer_list[2].question, self.questions[2])

            self.assertEqual(answer_list[0].answer_min, 2.0)
            self.assertEqual(answer_list[0].answer_max, 3.0)
            self.assertEqual(answer_list[1].answer_min, 1.0)
            self.assertEqual(answer_list[1].answer_max, 15.0)
            self.assertEqual(answer_list[2].answer, -1)

            self.assertFalse(field_list[0].answer)
            self.assertFalse(field_list[1].answer)
            self.assertTrue(field_list[2].answer)

            self.assertEqual(region_list[0].region.region_id, 1)
            self.assertEqual(region_list[1].region.region_id, 2)
            self.assertEqual(job_type_list[0].job_type.job_type_id, 1)
        # run tests described above
        test_db()

        # test illegal payloads
        data = json.dumps({
            'stuff' : 'nope'
        })
        request = self.factory.put('api/questions?student_id=2', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 406)
        test_db()

        data = json.dumps({
            'questions' : 'nope',
            'areas' : 'nope'
        })
        request = self.factory.put('api/questions?student_id=2', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 406)
        test_db()

        data = json.dumps({
            'questions' : [],
            'areas' : {'id' : 0}
        })
        request = self.factory.put('api/questions?student_id=2', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 406)
        test_db()

        data = json.dumps({
            'questions' : []
        })
        request = self.factory.put('api/questions?student_id=2', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 406)
        test_db()

        data = json.dumps({
            'questions' : [
                {'id' : 0, 'answer' : 12.0},
                {'id' : self.questions[2].pk, 'answer' : 5}
            ]
        })
        request = self.factory.put('api/questions?student_id=2', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 406)
        test_db()

        data = json.dumps({
            'looking_for' : [
                {'id' : 0, 'answer' : 12.0},
            ]
        })

        request = self.factory.put('api/questions?student_id=2', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 406)
        test_db()

        data = json.dumps({
            'regions' : [
                {'id' : 0, 'answer' : 12.0},
            ]
        })
        request = self.factory.put('api/questions?student_id=2', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 406)
        test_db()

        # test partial payloads
        data = json.dumps({
            'areas' : []
        })
        request = self.factory.put('api/questions?student_id=2', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 200)

        data = json.dumps({
            'looking_for' : []
        })
        request = self.factory.put('api/questions?student_id=2', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 200)


        data = json.dumps({
            'regions' : []
        })
        request = self.factory.put('api/questions?student_id=2', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 200)

        try:
            test_db()
        except AssertionError as error:
            self.assertEqual(str(error), 'False is not true')

        data = json.dumps({
            'questions' : [
                {'id' : 0},
                {'id' : self.questions[2].pk, 'answer' : 5},
                {'id' : self.questions[2].pk},
                {'id' : self.questions[1].pk, 'answer' : []},
                {'id' : self.questions[1].pk, 'answer' : {'min' : 1.5, 'max' : 2.5}}
            ],
            'areas' : [self.fields[2][0].pk]
        })
        request = self.factory.put('api/questions?student_id=2', data=data)
        response = views.questions(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('1/5 question answers' in str(response.content))  # only the last answer should be taken into account
        try:
            test_db()
        except AssertionError as error:
            self.assertEqual(str(error), '1.5 != 1.0')


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


class MatchingResultTestCase(TestCase):
    #This view currently assume that the machting algortim is done after returning 6 matches.
    def setUp(self):
        self.factory = RequestFactory()        
        current_fair = Fair.objects.create(name='Current fair', current=True)
        self.student1 = StudentProfile.objects.create(nickname='student1')
        self.student2 = StudentProfile.objects.create(nickname='student2')
        self.company1 = Company.objects.create(name='company1', organisation_number='1')
        self.company2 = Company.objects.create(name='company1', organisation_number='2')
        self.company3 = Company.objects.create(name='company1', organisation_number='3')
        self.company4 = Company.objects.create(name='company1', organisation_number='4')
        self.company5 = Company.objects.create(name='company1', organisation_number='5')
        self.company6 = Company.objects.create(name='company1', organisation_number='6')
        self.exhibitor1 = Exhibitor.objects.create(company=self.company1, fair=current_fair)
        self.exhibitor2 = Exhibitor.objects.create(company=self.company2, fair=current_fair)
        self.exhibitor3 = Exhibitor.objects.create(company=self.company3, fair=current_fair)
        self.exhibitor4 = Exhibitor.objects.create(company=self.company4, fair=current_fair)
        self.exhibitor5 = Exhibitor.objects.create(company=self.company5, fair=current_fair)
        self.exhibitor6 = Exhibitor.objects.create(company=self.company6, fair=current_fair)
    def test_view(self):
        #Returns empty list when no matching is done
        request = self.factory.get('/api/matching_result?student_id=1')
        response = views.matching_result(request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        matching = json.loads(response.content.decode(response.charset))
        self.assertEqual([], matching)

        #returns empty list when one matching is done
        matching_result1 = MatchingResult.objects.create(student=self.student1, exhibitor=self.exhibitor1, fair=Fair.objects.get(current=True), score=10)
        request = self.factory.get('/api/matching_result?student_id=1')
        response = views.matching_result(request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        matching = json.loads(response.content.decode(response.charset))
        self.assertEqual([], matching)

        #returns empty list when five matchings are done
        matching_result2 = MatchingResult.objects.create(student=self.student1, exhibitor=self.exhibitor2, fair=Fair.objects.get(current=True), score=0)
        matching_result3 = MatchingResult.objects.create(student=self.student1, exhibitor=self.exhibitor3, fair=Fair.objects.get(current=True), score=20)
        matching_result4 = MatchingResult.objects.create(student=self.student1, exhibitor=self.exhibitor4, fair=Fair.objects.get(current=True), score=100)
        matching_result5 = MatchingResult.objects.create(student=self.student1, exhibitor=self.exhibitor5, fair=Fair.objects.get(current=True), score=3)
        request = self.factory.get('/api/matching_result?student_id=1')
        response = views.matching_result(request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        matching = json.loads(response.content.decode(response.charset))
        self.assertEqual([], matching)

        #returns 5 matches when 6 matchings are done
        matching_result6 = MatchingResult.objects.create(student=self.student1, exhibitor=self.exhibitor6, fair=Fair.objects.get(current=True), score=70)
        request = self.factory.get('/api/matching_result?student_id=1')
        response = views.matching_result(request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        matching = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(matching), 5)
        #Should be in order
        self.assertEqual(matching[0]['percent'], 100)
        self.assertEqual(matching[1]['percent'], 70)
        self.assertEqual(matching[4]['percent'], 3)

        #still returns empty list for student2
        request = self.factory.get('/api/matching_result?student_id=2')
        response = views.matching_result(request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        matching = json.loads(response.content.decode(response.charset))
        self.assertEqual(matching, [])

        #returns 5 matches for studnet2 when 6 matchings are done
        matching_result6 = MatchingResult.objects.create(student=self.student2, exhibitor=self.exhibitor1, fair=Fair.objects.get(current=True), score=3)
        matching_result7 = MatchingResult.objects.create(student=self.student2, exhibitor=self.exhibitor2, fair=Fair.objects.get(current=True), score=3)
        matching_result8 = MatchingResult.objects.create(student=self.student2, exhibitor=self.exhibitor3, fair=Fair.objects.get(current=True), score=3)
        matching_result9 = MatchingResult.objects.create(student=self.student2, exhibitor=self.exhibitor4, fair=Fair.objects.get(current=True), score=3)
        matching_result10 = MatchingResult.objects.create(student=self.student2, exhibitor=self.exhibitor5, fair=Fair.objects.get(current=True), score=3)
        matching_result11 = MatchingResult.objects.create(student=self.student2, exhibitor=self.exhibitor6, fair=Fair.objects.get(current=True), score=3)
        request = self.factory.get('/api/matching_result?student_id=2')
        response = views.matching_result(request)
        self.assertEqual(response.status_code, HTTP_status_code_OK)
        matching = json.loads(response.content.decode(response.charset))
        self.assertEqual(len(matching), 5)

        #returns status code 404 if a student doesn't exists
        request = self.factory.get('/api/matching_result?student_id=5')
        response = views.matching_result(request)
        self.assertEqual(response.status_code, 404)







