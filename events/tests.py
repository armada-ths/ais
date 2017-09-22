from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User, Permission
from django.core.exceptions import PermissionDenied
from django.urls.exceptions import NoReverseMatch

from fair.models import Fair
from lib.image import load_test_image

from .models import Event


CURRENT_YEAR=timezone.now().year

test_urls = [
    '/fairs/'+str(CURRENT_YEAR)+'/events/',
    '/fairs/'+str(CURRENT_YEAR)+'/events/1/signup',
    '/fairs/'+str(CURRENT_YEAR)+'/events/1/unsignup',
    '/fairs/'+str(CURRENT_YEAR)+'/events/1/edit',
    '/fairs/'+str(CURRENT_YEAR)+'/events/1/attendants'
]


class EventTestCase(TestCase):

    fair=event=None

    # Kind of a workaround the error of permission denial.
    def assertPermissionDenied(self, client, url):
        try:
            response = client.get(url)
            self.fail('Permission was not denied') # we expect client.get() to throw an exception as working case, hence the fail statement
        except (PermissionDenied, NoReverseMatch):	
            return


    def setUp(self):
        self.fair = Fair.objects.create(name='Armada '+str(CURRENT_YEAR), year=CURRENT_YEAR, pk=2)
        
        self.event = Event.objects.create(
            fair=self.fair,
            name='Test event',
            capacity=12,
            event_start=timezone.now() + timezone.timedelta(days=2),
            event_end=timezone.now() + timezone.timedelta(days=3),
            registration_start=timezone.now() + timezone.timedelta(days=-1),
            registration_end=timezone.now() + timezone.timedelta(days=1),
            registration_last_day_cancel=timezone.now() + timezone.timedelta(days=2),
            pk=1,
        )

        self.admin_user = User.objects.create_user(username='admin', password='admin')
        self.basic_user = User.objects.create_user(username='user', password='user')

        permissions = {'add_event', 'change_event', 'delete_event'}
        for permission in permissions:
            self.admin_user.user_permissions.add(Permission.objects.get(codename=permission))


    def tearDown(self):
        self.fair.delete()
        self.event.delete()
        self.admin_user.delete()
        self.basic_user.delete()


    def test_no_login(self):
        client = Client()

        for url in test_urls:
            response = client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue('?next=' in response.url)


    def test_user(self):
        client = Client()
        response = client.post('/accounts/login/', { 'username':'user', 'password':'user'})
        self.assertEqual(response.status_code, 302)

        for i in range(1, 2):
            response = client.get(test_urls[i])
            self.assertEqual(response.status_code, 200)

        for i in range(2, len(test_urls)):
            self.assertPermissionDenied(client, test_urls[i])


    def test_admin(self):
        client = Client()
        response = client.post('/accounts/login/', { 'username':'admin', 'password':'admin' })
        self.assertEqual(response.status_code, 302)

        for i in range(0, len(test_urls)):
            if i == 2:
                continue
            response = client.get(test_urls[i])
            self.assertEqual(response.status_code, 200)

        self.assertPermissionDenied(client, test_urls[2])

        response = client.post(test_urls[3], {
            'name' :                            'Test event',
            'event_start' :                     str(timezone.now() + timezone.timedelta(days=2)).split('+')[0],
            'event_end' :                       str(timezone.now() + timezone.timedelta(days=3)).split('+')[0],
            'capacity' :                        12,
            'registration_start' :              str(timezone.now() + timezone.timedelta(days=-1)).split('+')[0],
            'registration_end' :                str(timezone.now() + timezone.timedelta(days=1)).split('+')[0],
            'registration_last_day_cancel' :    str(timezone.now() + timezone.timedelta(days=2)).split('+')[0],
            'image_original' :                  load_test_image(),
            'description' :                     'test desc'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('This field is required' not in str(response.content))
        self.assertEqual(Event.objects.get(pk=1).description, 'test desc')
        self.assertTrue(Event.objects.get(pk=1).image_original)
