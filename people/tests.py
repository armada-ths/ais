from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User, Permission
from django.core.exceptions import PermissionDenied
from django.urls.exceptions import NoReverseMatch

from fair.models import Fair
from .models import Profile
from lib.image import load_test_image


CURRENT_YEAR = timezone.now().year


class ProfileTestCase(TestCase):
    def setUp(self):
        fair = Fair.objects.create(
            name="Armada " + str(CURRENT_YEAR), year=CURRENT_YEAR, pk=2
        )

        self.now = timezone.now()
        self.tomorrow = self.now + timezone.timedelta(days=1)
        self.yesterday = self.now + timezone.timedelta(days=-1)

        self.admin_user = User.objects.create_user(username="admin", password="admin")
        self.basic_user = User.objects.create_user(username="user", password="user")

        permissions = [
            "view_people",
        ]

        for permission in permissions:
            self.admin_user.user_permissions.add(
                Permission.objects.get(codename=permission)
            )

    def test_profiles_no_login(self):
        # We expect to always be redirected to the login screen

        client = Client()
        response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/")

        self.assertEqual(response.status_code, 302)
        self.assertTrue("?next=" in response.url)

        response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/1")
        self.assertEqual(response.status_code, 302)
        self.assertTrue("?next=" in response.url)

        response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/1")
        self.assertEqual(response.status_code, 302)
        self.assertTrue("?next=" in response.url)

        response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/2")
        self.assertEqual(response.status_code, 302)
        self.assertTrue("?next=" in response.url)

        response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/2")
        self.assertEqual(response.status_code, 302)
        self.assertTrue("?next=" in response.url)

    def test_profile_create(self):
        profile = Profile(user=self.basic_user)
        self.assertTrue(profile)

    def test_profiles_user(self):
        client = Client()
        response = client.post(
            "/accounts/login/", {"username": "user", "password": "user"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue("/accounts/profile/" in response.url)

        try:
            response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/")
            self.assertTrue(
                False
            )  # exception is the expected behavior, hence the weird assert
        except (PermissionDenied, NoReverseMatch):
            pass

        try:
            response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/1")
            self.assertTrue(
                False
            )  # exception is the expected behavior, hence the weird assert
        except (PermissionDenied, NoReverseMatch):
            pass

        response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/2")
        self.assertEqual(response.status_code, 200)

        try:
            response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/1/edit")
            self.assertTrue(
                False
            )  # exception is the expected behavior, hence the weird assert
        except (PermissionDenied, NoReverseMatch):
            pass

        response = client.post(
            "/fairs/" + str(CURRENT_YEAR) + "/people/2/edit",
            {
                "phone_number": "123456789",
                "picture_original": load_test_image(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEquals(
            User.objects.get(username="user").profile.phone_number, "123456789"
        )
        self.assertTrue(User.objects.get(username="user").profile.picture_original)

    def test_profiles_admin(self):
        client = Client()
        response = client.post(
            "/accounts/login/", {"username": "admin", "password": "admin"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue("/accounts/profile/" in response.url)

        response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/")
        self.assertEqual(response.status_code, 200)

        response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/1")
        self.assertEqual(response.status_code, 200)

        response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/2")
        self.assertEqual(response.status_code, 200)

        response = client.post(
            "/fairs/" + str(CURRENT_YEAR) + "/people/1/edit",
            {
                "phone_number": "123456789",
                "picture_original": load_test_image(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEquals(
            User.objects.get(username="admin").profile.phone_number, "123456789"
        )
        self.assertTrue(User.objects.get(username="admin").profile.picture_original)

        try:
            response = client.get("/fairs/" + str(CURRENT_YEAR) + "/people/2/edit")
            self.assertTrue(
                False
            )  # exception is the expected behavior, hence the weird assert
        except (PermissionDenied, NoReverseMatch):
            pass
