from django.test import TestCase
from .models import InterviewQuestion, RecruitmentPeriod
from fair.models import Fair
from django.utils import timezone

# Create your tests here.

class RecruitmentTestCase(TestCase):
    def setUp(self):
        fair = Fair.objects.create(name="Armada 2016")
        recruitmentPeriod = RecruitmentPeriod.objects.create(name="PG", start_date=timezone.now(), end_date=timezone.now(), fair=fair)
        InterviewQuestion.objects.create(recruitmentPeriod=recruitmentPeriod)

    def test_arguments_as_list(self):
        interviewQuestion = InterviewQuestion.objects.all().first()
        self.assertEqual(interviewQuestion.fieldType, 0)
