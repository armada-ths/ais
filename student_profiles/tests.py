from django.test import TestCase

from fair.models import Fair
from companies.models import Company
from exhibitors.models import Exhibitor

from .models import StudentProfile, MatchingResult

class MatchingResultTestCase(TestCase):
    '''
    For now only tests if a matching result with its foregin keys can be created
    and filtered on
    '''

    def setUp(self):
        self.fair = Fair.objects.create(name='Armada 2017', year='2017', pk=1337, current=True)
        self.company0 = Company.objects.create(name='TestCompany1', organisation_type='company')
        self.company1 = Company.objects.create(name='TestCompany2', organisation_type='company')
        self.exhibitor0 = Exhibitor.objects.create(company=self.company0, fair=self.fair)
        self.exhibitor1 = Exhibitor.objects.create(company=self.company1, fair=self.fair)
        self.student0 = StudentProfile.objects.create(nickname='Askel')
        self.student1 = StudentProfile.objects.create(nickname='Gringo')

        matchingresults = []
        for i in range(2):
            for j in range(2):
                mr = MatchingResult.objects.create(fair=self.fair, score=(i+j)*10,
                    student=eval('self.student%i'%i),
                    exhibitor=eval('self.exhibitor%i'%j))
                matchingresults.append(mr)
        self.matchingresults = matchingresults

    def test_model(self):
        ''' test if model is set up correctly '''
        matchingresults = list(MatchingResult.objects.filter(fair=self.fair))
        self.assertEqual(len(matchingresults), 4)

        matchingresults_filtered = list(MatchingResult.objects.filter(fair=self.fair, exhibitor__in=[self.exhibitor0]))
        self.assertTrue(self.matchingresults[0] in matchingresults_filtered)
        self.assertTrue(self.matchingresults[2] in matchingresults_filtered)
        self.assertFalse(self.matchingresults[1] in matchingresults_filtered)
        self.assertFalse(self.matchingresults[3] in matchingresults_filtered)
        self.assertEqual(len(matchingresults_filtered),2)
