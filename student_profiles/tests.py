from django.test import TestCase

from fair.models import Fair
from companies.models import Company

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
        self.student0 = StudentProfile.objects.create(nickname='Askel')
        self.student1 = StudentProfile.objects.create(nickname='Gringo')

        matchingresults = []
        for i in range(2):
            for j in range(2):
                mr = MatchingResult.objects.create(fair=self.fair, score=(i+j)*10,
                    student=eval('self.student%i'%i),
                    company=eval('self.company%i'%j))
                matchingresults.append(mr)
        self.matchingresults = matchingresults

    def test_model(self):
        ''' test if model is set up correctly '''
        matchingresults = list(MatchingResult.objects.filter(fair=self.fair))
        self.assertEqual(len(matchingresults), 4)

        matchingresults_filtered = list(MatchingResult.objects.filter(fair=self.fair, company__in=[self.company0]))
        self.assertTrue(self.matchingresults[0] in matchingresults_filtered)
        self.assertTrue(self.matchingresults[2] in matchingresults_filtered)
        self.assertFalse(self.matchingresults[1] in matchingresults_filtered)
        self.assertFalse(self.matchingresults[3] in matchingresults_filtered)
        self.assertEqual(len(matchingresults_filtered),2)
