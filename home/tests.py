from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse


class HomeIndexViewTests(TestCase):
    def test_anonymous_user_gets_sign_in_up_links(self):
        response = self.client.get('/')
        self.assertContains(response, "Log In")
        self.assertContains(response, "Sign Up")

    def test_signed_in_user_username(self):
        username = "JimboBaggins"
        email = "jbaggins@test.com"
        password = "password"
        User.objects.create_user(username=username, email=email, password=password)
        response = self.client.post('/login/', {'username': username, 'password': password})
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/')
        self.assertContains(response, username)
