

from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import PermissionDenied
from django.urls.exceptions import NoReverseMatch

from fair.models import Fair
from lib.image import load_test_image

from .models import RecruitmentPeriod, RecruitmentApplication, Role, RoleApplication, Programme


class RecruitmentTestCase(TestCase):
    def setUp(self):
        fair = Fair.objects.create(name="Armada 2016", year=2016, pk=2)

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
        self.core_user = User.objects.create_user(username='core', password='core')

        self.pg_role = Role.objects.create(name='PG', pk=1)
        self.core_group_role = Role.objects.create(name="Project Core Team",pk=33333333)
        self.system_developer = Role.objects.create(name='System Developer', parent_role=self.pg_role, pk=2)



        pg_permissions = [
            'view_recruitment_applications', 'view_recruitment_interviews', 'administer_recruitment_applications',
            'administer_roles', 'administer_recruitment']

        for permission in pg_permissions:
            Group.objects.get(name='PG').permissions.add(Permission.objects.get(codename=permission))


        self.career_fair_leader = Role.objects.create(name='Career Fair Leader', pk=3)

        self.recruitment_period.recruitable_roles.add(self.system_developer, self.career_fair_leader)

        self.recruitment_application = RecruitmentApplication.objects.create(
            pk=1337,
            user=self.purmonen_user,
            recruitment_period=self.recruitment_period
        )

        self.recruitment_application = RecruitmentApplication.objects.create(
            pk=2000,
            user=self.core_user,
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
        self.pg_role.add_user_to_groups(self.purmonen_user)
        self.core_group_role.add_user_to_groups(self.core_user)
        self.pg_role.add_user_to_groups(self.core_user)


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

        self.assertTrue('recruitment.administer_recruitment' in self.purmonen_user.get_all_permissions())
        self.assertTrue('recruitment.administer_roles' in self.purmonen_user.get_all_permissions())



    def test_site_for_non_armada_member(self):

        client = Client()
        response = client.post('/accounts/login/', {'username': 'bratteby', 'password': 'bratteby'})
        response = client.get('/fairs/2016/recruitment/')

        self.assertEqual(response.status_code, 200)

        try:
            response = client.get('/fairs/2016/recruitment/new')
        except (PermissionDenied, NoReverseMatch):
            pass

        response = client.get('/fairs/2016/recruitment/%d' % self.recruitment_period.pk)
        self.assertEqual(response.status_code, 200)

        response = client.get('/fairs/2016/recruitment/%d/application/1337' % self.recruitment_period.pk)
        self.assertEqual(response.status_code, 200)

        try:
            response = client.get('/fairs/2016/recruitment/%d/application/1337/interview' % self.recruitment_period.pk)
        except (PermissionDenied, NoReverseMatch):
            pass

        response = client.get('/fairs/2016/recruitment/roles/1')
        self.assertEqual(response.status_code, 200)

    def test_site_for_armada_member(self):
        client = Client()
        response = client.post('/accounts/login/', {'username': 'purmonen', 'password': 'purmonen'})
        response = client.get('/fairs/2016/recruitment/')
        self.assertEqual(response.status_code, 200)

        response = client.get('/fairs/2016/recruitment/new')
        self.assertEqual(response.status_code, 200)

        response = client.get('/fairs/2016/recruitment/new')
        self.assertEqual(response.status_code, 200)


        # log in to user that is in core project team
        response = client.post('/accounts/login/', {'username': 'core', 'password': 'core'})
        response = client.get('/fairs/2016/recruitment/')
        self.assertEqual(response.status_code, 200)

        # member of project core team should be able to
        # enter a recruitment period (also interviews in it) with their application in it
        response = client.get('/fairs/2016/recruitment/%d' % self.recruitment_period.pk)
        self.assertEqual(response.status_code, 200)

        response = client.get('/fairs/2016/recruitment/%d/application/1337/interview' % self.recruitment_period.pk)
        self.assertEqual(response.status_code, 200)

        # log in to other user again
        response = client.post('/accounts/login/', {'username': 'purmonen', 'password': 'purmonen'})
        response = client.get('/fairs/2016/recruitment/')
        self.assertEqual(response.status_code, 200)

        response = client.get('/fairs/2016/recruitment/%d/application/1337' % self.recruitment_period.pk)
        self.assertEqual(response.status_code, 200)

        response = client.get('/fairs/2016/recruitment/%d/application/1337/interview' % self.recruitment_period.pk)
        self.assertEqual(response.status_code, 403)

        response = client.get('/fairs/2016/recruitment/roles/1')
        self.assertEqual(response.status_code, 200)

    def test_create_application(self):
        self.recruitment_period.end_date = self.tomorrow
        self.recruitment_period.save()

        client = Client()
        self.assertEquals(len(self.recruitment_period.recruitmentapplication_set.all()), 2)

        response = client.post('/accounts/login/', {'username': 'bratteby', 'password': 'bratteby'})
        response = client.post('/fairs/2016/recruitment/%d/application/new' % self.recruitment_period.pk, {
            'username': 'purmonen', 'password': 'purmonen'
        })
        self.assertTrue('This field is required' in str(response.content))

        self.assertEquals(len(self.recruitment_period.recruitmentapplication_set.all()), 2)
        response = client.post('/fairs/2016/recruitment/1/application/new', {
            'role1': '3',
            'programme': '1',
            'registration_year': '2016',
            'phone_number': '0735307028',
        })

        self.assertTrue('This field is required' not in str(response.content))
        self.assertEquals(len(self.recruitment_period.recruitmentapplication_set.all()), 3)


        recruitment_application = RecruitmentApplication.objects.get(user=self.bratteby_user)
        self.assertEquals(User.objects.get(username='bratteby').profile.phone_number, '0735307028')
        self.assertEquals(RecruitmentApplication.objects.get(user=self.bratteby_user).roleapplication_set.get(order=0).role.pk, 3)

        response = client.post('/fairs/2016/recruitment/1/application/%d' % recruitment_application.pk, {
            'role1': '2',
            'programme': '1',
            'registration_year': '2016',
            'phone_number': '0735307029',
            'picture_original': load_test_image()
        })

        self.assertTrue('This field is required' not in str(response.content))
        self.assertEquals(len(self.recruitment_period.recruitmentapplication_set.all()), 3)
        self.assertEquals(User.objects.get(username='bratteby').profile.phone_number, '0735307029')
        self.assertTrue(User.objects.get(username='bratteby').profile.picture_original)

        self.assertEquals(
            RecruitmentApplication.objects.get(user=self.bratteby_user).roleapplication_set.get(order=0).role.pk, 2)


    def test_create_recruitment_period(self):
        client = Client()

        response = client.post('/accounts/login/', {'username': 'bratteby', 'password': 'bratteby'})

        self.assertEquals(len(RecruitmentPeriod.objects.all()), 1)
        try:
            response = client.post('/fairs/2016/recruitment/new', {
                'name': 'Host Recruitment',
                'eligible_roles': '2',
                'fair': '2',
                'start_date': '2016-01-1',
                'end_date': '2016-01-2',
                'interview_end_date': '2016-01-3'
            })
            self.assertTrue(False)
        except (PermissionDenied, NoReverseMatch):
            # This is expected
            pass

        self.assertEquals(len(RecruitmentPeriod.objects.all()), 1)
        #self.assertEquals(response.status_code, 403)

        response = client.post('/accounts/login/', {'username': 'purmonen', 'password': 'purmonen'})


        response = client.post('/fairs/2016/recruitment/new', {
            'name': 'Host Recruitment',
            'eligible_roles': '2',
            'fair': '2',
            'start_date': '2016-01-1',
            'end_date': '2016-01-2',
            'interview_end_date': '2016-01-3'
        })
        self.assertEquals(len(RecruitmentPeriod.objects.all()), 2)




def check_users():
    users_with_roles = [(user, user.recruitmentapplication_set.filter(status='accepted').first()) for user in User.objects.all()]
    len(users_with_roles)

    accepted_users_with_roles = [
        user_with_role for user_with_role in users_with_roles if user_with_role[1] and user_with_role[1].status == 'accepted']
    len(accepted_users_with_roles)


    accepted_users_without_role_or_group = [user_with_role for user_with_role in accepted_users_with_roles if not user_with_role[1].delegated_role or not user_with_role[0].groups.filter(name=user_with_role[1].delegated_role.name).first()]
    len(accepted_users_without_role_or_group)

    accepted_users_with_not_2_groups = [user for user in accepted_users_with_roles if len(user[0].groups.all()) != 2]
    len(accepted_users_with_not_2_groups)
