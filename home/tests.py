from django.test import TestCase
from django.contrib.auth import authenticate
from user.models import User
from django.urls import reverse
from datetime import date


class HomeIndexViewTests(TestCase):
    def test_anonymous_user_gets_sign_in_up_links(self):
        response = self.client.get('/')
        self.assertContains(response, "Log In")
        self.assertContains(response, "Sign Up")

    def test_signed_in_user_username(self):
        username = "JimboBaggins"
        email = "jbaggins@test.com"
        password = "password"
        birth_date = date(2002, 8, 3)
        User.objects.create_user(username=username, email=email, password=password, birth_date=birth_date)
        response = self.client.post(reverse("user:login"), {'username': username, 'password': password, })
        self.assertEquals(response.status_code, 302)
        response = self.client.get('/')
        self.assertContains(response, username)
