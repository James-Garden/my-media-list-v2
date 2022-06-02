from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


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
