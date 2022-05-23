from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse


class HomeIndexViewTests(TestCase):
    def test_anonymous_user_gets_sign_in_up_links(self):
        response = self.client.get(reverse('home:index'))
        self.assertContains(response, "Log In")
        self.assertContains(response, "Sign Up")

