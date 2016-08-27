from django.test import TestCase
from .models import RecruitmentPeriod, RecruitmentApplication
from fair.models import Fair
from django.utils import timezone
from django.contrib.auth.models import User

# Create your tests here.

class RecruitmentTestCase(TestCase):


    def setUp(self):
        fair = Fair.objects.create(name="Armada 2016")

        self.now = timezone.now()
        self.tomorrow = self.now + timezone.timedelta(days=1)
        self.yesterday = self.now + timezone.timedelta(days=-1)

        self.recruitment_period = RecruitmentPeriod.objects.create(
            name="PG",
            start_date=self.yesterday,
            end_date=self.yesterday,
            interview_end_date=self.yesterday,
            fair=fair)

        self.purmonen_user = User.objects.create(username='purmonen')
        self.bratteby_user = User.objects.create(username='bratteby')

        self.recruitment_application = RecruitmentApplication.objects.create(
            user=self.purmonen_user,
            recruitment_period=self.recruitment_period
        )


    def test_recruitment_period(self):
        self.assertNotEqual(self.recruitment_period.interview_questions, None)
        self.assertNotEqual(self.recruitment_period.application_questions, None)

        self.assertEqual(self.recruitment_period.is_past(), True)
        self.assertEqual(self.recruitment_period.is_future(), False)

        self.recruitment_period.start_date = self.tomorrow
        self.recruitment_period.end_date = self.tomorrow


        self.assertEqual(self.recruitment_period.is_past(), False)
        self.assertEqual(self.recruitment_period.is_future(), True)


    def test_recruitment_application(self):
        self.assertEqual(self.recruitment_application.status, None)
        self.assertEqual(self.recruitment_application.state(), 'new')

        self.recruitment_application.interviewer = self.bratteby_user
        self.assertEqual(self.recruitment_application.state(), 'interview_delegated')

        self.recruitment_application.interview_date = self.tomorrow
        self.assertEqual(self.recruitment_application.state(), 'interview_planned')

        self.recruitment_application.interview_date = self.yesterday
        self.assertEqual(self.recruitment_application.state(), 'interview_done')

