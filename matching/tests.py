from django.test import TestCase
from fair.models import Fair
from companies.models import Company
from exhibitors.models import Exhibitor
from .models import Survey, Question, Response, TextAns, ChoiceAns, IntegerAns, BooleanAns

class MatchingTestCase(TestCase):
    ''' Tests the filtering on questions and answers to different surveys, also
        test that questions that belongs to multiple surveys are found for
    '''
    def setUp(self):
        self.fair_current = Fair.objects.create(name='Armada 2017',
                                        year='2017',
                                        pk=1337,
                                        current=True)
        self.fair_old = Fair.objects.create(name='Armada 2016',
                                        year='2016',
                                        pk=1336,
                                        current=False)
        self.survey_current = Survey.objects.create(fair=self.fair_current, name='survey2017')
        self.survey_old = Survey.objects.create(fair=self.fair_old, name='survey2016')
        self.q2017 = Question.objects.create(   text='q2017',
                                                question_type=Question.TEXT,
                                                name='q2017')
        self.q2017.survey.add(self.survey_current)
        self.q2016 = Question.objects.create(   text='q2016',
                                                question_type=Question.TEXT,
                                                name='q2016')
        self.q2016.survey.add(self.survey_old)
        self.q_mix = Question.objects.create(   text='qmix',
                                                question_type=Question.TEXT,
                                                name='qmix')
        self.q_mix.survey.add(self.survey_current)
        self.q_mix.survey.add(self.survey_old)

        self.company = Company.objects.create(name="TestCompany1", organisation_type='company')
        self.exhibitor_current = Exhibitor.objects.create(company=self.company, fair=self.fair_current)
        self.exhibitor_old = Exhibitor.objects.create(company=self.company, fair=self.fair_old)

        self.resp_old = Response.objects.create(exhibitor=self.exhibitor_old, question=self.q2016)
        self.ans_old = TextAns.objects.create(question=self.q2016, response=self.resp_old)

        self.resp_current = Response.objects.create(exhibitor=self.exhibitor_current, question=self.q2017)
        self.ans_current = TextAns.objects.create(question=self.q2017, response=self.resp_current)

        self.resp_current_on_mixed = Response.objects.create(exhibitor=self.exhibitor_current, question=self.q_mix)
        self.ans_current_on_mixed = TextAns.objects.create(question=self.q_mix, response=self.resp_current_on_mixed)

        self.resp_old_on_mixed = Response.objects.create(exhibitor=self.exhibitor_old, question=self.q_mix)
        self.ans_old_on_mixed = TextAns.objects.create(question=self.q_mix, response=self.resp_old_on_mixed)

    def test_correct_filter(self):
        ''' Tests if the db is set up correctly by checkint if questions,
            responses, answers are returned correctly. Especielly check for
            questions that below to multiple surveys but to exhibitors from
            different years
        '''

        q_current       = Question.objects.filter(survey=self.survey_current)
        q_old           = Question.objects.filter(survey=self.survey_old)
        resp_current    = Response.objects.filter(question__in=q_current, exhibitor__in=[self.exhibitor_current])
        resp_old        = Response.objects.filter(question__in=q_old, exhibitor__in=[self.exhibitor_old])

        ans_current     = TextAns.objects.filter(response__in=resp_current)
        ans_old         = TextAns.objects.filter(response__in=resp_old)

        self.assertEqual(list(q_current), [self.q2017, self.q_mix])
        self.assertEqual(list(q_old), [self.q2016, self.q_mix])
        self.assertEqual(list(resp_current), [self.resp_current, self.resp_current_on_mixed])
        self.assertEqual(list(resp_old), [self.resp_old, self.resp_old_on_mixed])
        self.assertEqual(list(ans_current), [self.ans_current, self.ans_current_on_mixed])
        self.assertEqual(list(ans_old), [self.ans_old, self.ans_old_on_mixed])
