from django.test import TestCase
from .models import RecruitmentPeriod, RecruitmentApplication, Role, RoleApplication, AISPermission, Programme
from fair.models import Fair
from django.utils import timezone
from django.contrib.auth.models import User

from django.test import Client

# Create your tests here.

class RecruitmentTestCase(TestCase):


    def setUp(self):
        fair = Fair.objects.create(name="Armada 2016", year=timezone.now().year, pk=2)

        self.now = timezone.now()
        self.tomorrow = self.now + timezone.timedelta(days=1)
        self.yesterday = self.now + timezone.timedelta(days=-1)


        Programme.objects.create(
            name='Computer Science',
            pk=1,
        )

        self.recruitment_period = RecruitmentPeriod.objects.create(
            name="PG",
            start_date=self.yesterday,
            end_date=self.yesterday,
            interview_end_date=self.yesterday,
            fair=fair)

        self.purmonen_user = User.objects.create_user(username='purmonen', password='purmonen')
        self.bratteby_user = User.objects.create_user(username='bratteby', password='bratteby')


        self.pg_role = Role.objects.create(name='PG', pk=1)
        self.system_developer = Role.objects.create(name='System Developer', parent_role=self.pg_role, pk=2)
        self.career_fair_leader = Role.objects.create(name='Career Fair Leader', pk=3)

        self.administer_roles_permission = AISPermission.objects.create(codename='administer_roles', name='Administer roles')
        self.administer_recruitment_permission = AISPermission.objects.create(codename='administer_recruitment', name='Administer recruitment')
        self.view_recruitment_applications_permission = AISPermission.objects.create(codename='view_recruitment_applications',
                                                                              name='View recruitment applications')
        self.view_recruitment_interviews_permission = AISPermission.objects.create(
            codename='view_recruitment_interviews',
            name='View recruitment interviews')

        self.pg_role.permissions.add(self.administer_roles_permission)
        self.pg_role.permissions.add(self.administer_roles_permission)
        self.pg_role.permissions.add(self.view_recruitment_applications_permission)
        self.system_developer.permissions.add(self.administer_recruitment_permission)
        self.system_developer.permissions.add(self.view_recruitment_interviews_permission)
        self.career_fair_leader.permissions.add(self.administer_recruitment_permission)

        self.recruitment_period.recruitable_roles.add(self.system_developer, self.career_fair_leader)

        self.recruitment_application = RecruitmentApplication.objects.create(
            pk=1337,
            user=self.purmonen_user,
            recruitment_period=self.recruitment_period
        )

        RoleApplication.objects.create(
            recruitment_application=self.recruitment_application,
            role=self.system_developer,
            order=2
        )

        RoleApplication.objects.create(
            recruitment_application=self.recruitment_application,
            role=self.career_fair_leader,
            order=1
        )


    def test_recruitment_period(self):

        self.assertEqual(len(self.recruitment_period.recruitable_roles.all()), 2)

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

        self.recruitment_application.delegated_role = self.system_developer
        self.assertEqual(self.recruitment_application.state(), 'interview_done')

        self.recruitment_application.status = 'accepted'
        self.assertEqual(self.recruitment_application.state(), 'accepted')

        self.recruitment_application.save()

        self.assertTrue('administer_recruitment' in self.purmonen_user.ais_permissions())
        self.assertTrue('administer_roles' in self.purmonen_user.ais_permissions())

        self.recruitment_application.delegated_role = self.career_fair_leader
        self.recruitment_application.save()

        self.assertTrue('administer_recruitment' in self.purmonen_user.ais_permissions())
        self.assertTrue('administer_roles' not in self.purmonen_user.ais_permissions())

        self.recruitment_application.status = 'rejected'
        self.recruitment_application.save()
        self.assertEqual(self.recruitment_application.state(), 'rejected')

        self.assertTrue('administer_recruitment' not in self.purmonen_user.ais_permissions())
        self.assertTrue('administer_roles' not in self.purmonen_user.ais_permissions())


    def test_site_for_non_armada_member(self):
        self.recruitment_application.status = 'rejected'
        self.recruitment_application.save()

        client = Client()
        response = client.post('/accounts/login/', {'username': 'purmonen', 'password': 'purmonen'})
        response = client.get('/recruitment/')

        self.assertEqual(response.status_code, 200)

        response = client.get('/recruitment/new')
        self.assertEqual(response.status_code, 403)

        response = client.get('/recruitment/%d' % self.recruitment_period.pk)
        self.assertEqual(response.status_code, 200)

        response = client.get('/recruitment/%d/application/1337' % self.recruitment_period.pk)
        self.assertEqual(response.status_code, 200)

        response = client.get('/recruitment/%d/application/1337/interview' % self.recruitment_period.pk)
        self.assertEqual(response.status_code, 403)

        response = client.get('/recruitment/roles/1')
        self.assertEqual(response.status_code, 200)

    def test_site_for_armada_member(self):
        self.recruitment_application.delegated_role = self.system_developer
        self.recruitment_application.status = 'accepted'
        self.recruitment_application.save()

        client = Client()
        response = client.post('/accounts/login/', {'username': 'purmonen', 'password': 'purmonen'})
        response = client.get('/recruitment/')
        self.assertEqual(response.status_code, 200)

        response = client.get('/recruitment/new')
        self.assertEqual(response.status_code, 200)

        response = client.get('/recruitment/new')
        self.assertEqual(response.status_code, 200)

        response = client.get('/recruitment/%d' % self.recruitment_period.pk)
        self.assertEqual(response.status_code, 200)

        response = client.get('/recruitment/%d/application/1337' % self.recruitment_period.pk)
        self.assertEqual(response.status_code, 200)

        response = client.get('/recruitment/%d/application/1337/interview' % self.recruitment_period.pk)
        self.assertEqual(response.status_code, 200)

        response = client.get('/recruitment/roles/1')
        self.assertEqual(response.status_code, 200)

    def test_create_application(self):
        self.recruitment_period.end_date = self.tomorrow
        self.recruitment_period.save()

        client = Client()
        self.assertEquals(len(self.recruitment_period.recruitmentapplication_set.all()), 1)

        response = client.post('/accounts/login/', {'username': 'bratteby', 'password': 'bratteby'})
        response = client.post('/recruitment/%d/application/new' % self.recruitment_period.pk, {
            'username': 'purmonen', 'password': 'purmonen'
        })
        self.assertTrue('This field is required' in str(response.content))

        self.assertEquals(len(self.recruitment_period.recruitmentapplication_set.all()), 1)
        response = client.post('/recruitment/1/application/new', {
            'role1': '3',
            'programme': '1',
            'registration_year': '2016',
            'phone_number': '0735307028',
        })

        self.assertTrue('This field is required' not in str(response.content))
        self.assertEquals(len(self.recruitment_period.recruitmentapplication_set.all()), 2)


        recruitment_application = RecruitmentApplication.objects.get(user=self.bratteby_user)
        self.assertEquals(User.objects.get(username='bratteby').profile.phone_number, '0735307028')
        self.assertEquals(RecruitmentApplication.objects.get(user=self.bratteby_user).roleapplication_set.get(order=0).role.pk, 3)

        response = client.post('/recruitment/1/application/%d' % recruitment_application.pk, {
            'role1': '2',
            'programme': '1',
            'registration_year': '2016',
            'phone_number': '0735307029',
        })

        self.assertTrue('This field is required' not in str(response.content))
        self.assertEquals(len(self.recruitment_period.recruitmentapplication_set.all()), 2)
        self.assertEquals(User.objects.get(username='bratteby').profile.phone_number, '0735307029')

        self.assertEquals(
            RecruitmentApplication.objects.get(user=self.bratteby_user).roleapplication_set.get(order=0).role.pk, 2)


    def test_create_recruitment_period(self):
        client = Client()

        response = client.post('/accounts/login/', {'username': 'purmonen', 'password': 'purmonen'})

        # Test without having recruitment administration permission
        self.recruitment_application.delegated_role = self.system_developer
        self.recruitment_application.status = 'rejected'
        self.recruitment_application.save()

        self.assertEquals(len(RecruitmentPeriod.objects.all()), 1)
        response = client.post('/recruitment/new', {
            'name': 'Host Recruitment',
            'eligible_roles': '2',
            'fair': '2',
            'start_date': '2016-01-1',
            'end_date': '2016-01-2',
            'interview_end_date': '2016-01-3'
        })
        self.assertEquals(len(RecruitmentPeriod.objects.all()), 1)
        self.assertEquals(response.status_code, 403)
        self.recruitment_application.status = 'accepted'
        self.recruitment_application.save()


        response = client.post('/recruitment/new', {
            'name': 'Host Recruitment',
            'eligible_roles': '2',
            'fair': '2',
            'start_date': '2016-01-1',
            'end_date': '2016-01-2',
            'interview_end_date': '2016-01-3'
        })
        self.assertEquals(len(RecruitmentPeriod.objects.all()), 2)

