from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class LoginTests(TestCase):
    def test_login_view_loads(self):
        response = self.client.get(reverse("user:login"))
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        username = "bilbo"
        password = "swaggins"
        User.objects.create_user(username, 'bbaggins@theshire.com', password)
        response = self.client.post(reverse("user:login"), {'username': 'user', 'password': 'password'})
        self.assertNotContains(response, username)

    def test_invalid_login_alert(self):
        response = self.client.post(reverse("user:login"), {'username': 'user', 'password': 'password'})
        self.assertContains(response, '<div class="alert')

    def test_valid_login(self):
        username = "bilbo"
        password = "swaggins"
        User.objects.create_user(username, 'bbaggins@theshire.com', password)
        response = self.client.post(reverse("user:login"), {'username': username, 'password': password}, follow=True)
        self.assertContains(response, username)


class RegistrationTests(TestCase):
    def test_registration_view_loads(self):
        response = self.client.get(reverse('user:registration'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_redirected(self):
        # Create test user
        username = "reg_redirect_test_user"
        password = "password"
        User.objects.create_user(username, "email@example.com", password)
        # Log in test user
        self.client.post(reverse("user:login"), {'username': username, 'password': password})
        # Test redirect
        response = self.client.get(reverse('user:registration'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("user:profile"))

    def test_no_info_register(self):
        response = self.client.post(reverse("user:registration"))
        self.assertContains(response, "This field is required.")

    def test_missing_field_register(self):
        response = self.client.post(reverse("user:registration"), {
            'username': "test_username",
            'password1': "test_password",
            'password2': "test_password",
        })
        self.assertContains(response, 'This field is required.')

    def test_invalid_field_register(self):
        response = self.client.post(reverse("user:registration"), {
            'username': "test_username",
            'password1': "test_password",
            'password2': "test_password",
            'email': "!",
            'birth_date': "01/01/1999",
        })
        self.assertContains(response, "Enter a valid email address.")

    def test_valid_register(self):
        response = self.client.post(reverse("user:registration"), {
            'username': "Test_username",
            'password1': "test_password",
            'password2': "test_password",
            'email': "email@example.com",
            'birth_date': "01/01/1999",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("user:profile"))

    def test_invalid_date_format(self):
        response = self.client.post(reverse("user:registration"), {
            'username': "Test_username",
            'password1': "test_password",
            'password2': "test_password",
            'email': "email@example.com",
            'birth_date': "01-01-1999",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid date.")

    def test_dob_too_recent(self):
        # Someone who was born today should not be allowed to register
        response = self.client.post(reverse("user:registration"), {
            'username': "Test_username",
            'password1': "test_password",
            'password2': "test_password",
            'email': "email@example.com",
            'birth_date': datetime.strftime(datetime.now(), "%d/%m/%Y"),
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You must be at least 13 years old.")

    def test_dob_thirteen_years(self):
        # Someone who has just turned 13 should be allowed to register
        response = self.client.post(reverse("user:registration"), {
            'username': "Test_username",
            'password1': "test_password",
            'password2': "test_password",
            'email': "email@example.com",
            'birth_date': datetime.strftime(datetime.now() - timedelta(days=35152), "%d/%m/%Y"),
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("user:profile"))
