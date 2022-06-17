from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse
from user.models import User
from datetime import datetime, date, timedelta
from django.core.management import call_command


class LoginTests(TestCase):
    def test_login_view_loads(self):
        response = self.client.get(reverse("user:login"))
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        username = "bilbo"
        password = "swaggins"
        birth_date = date(2002, 8, 3)
        User.objects.create_user(username, 'bbaggins@theshire.com', password, birth_date=birth_date)
        response = self.client.post(reverse("user:login"), {'username': 'user', 'password': 'password'})
        self.assertNotContains(response, username)

    def test_invalid_login_alert(self):
        response = self.client.post(reverse("user:login"), {'username': 'user', 'password': 'password'})
        self.assertContains(response, '<div class="alert')

    def test_valid_login(self):
        username = "bilbo"
        password = "swaggins"
        birth_date = date(2002, 8, 3)
        User.objects.create_user(username, 'bbaggins@theshire.com', password, birth_date=birth_date)
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
        birth_date = date(2002, 8, 3)
        User.objects.create_user(username, "email@example.com", password, birth_date=birth_date)
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
        dob = datetime.now().date()
        dob = dob.replace(year=(dob.year - 13))
        response = self.client.post(reverse("user:registration"), {
            'username': "Test_username",
            'password1': "test_password",
            'password2': "test_password",
            'email': "email@example.com",
            'birth_date': dob,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("user:profile"))

    def test_dob_not_thirteen_years(self):
        # Someone who has just turned 13 should be allowed to register
        dob = datetime.now().date()
        dob.replace(year=dob.year - 13, day=dob.day - 1)
        dob.replace(year=dob.day - 1)
        response = self.client.post(reverse("user:registration"), {
            'username': "Test_username",
            'password1': "test_password",
            'password2': "test_password",
            'email': "email@example.com",
            'birth_date': dob,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You must be at least 13 years old.")


class UserModelTests(TestCase):
    @staticmethod
    def create_valid_user():
        username = "Bilbo"
        password = "swaggins"
        birth_date = date(2002, 8, 3)
        return User.objects.create_user(username, 'bbaggins@theshire.com', password, birth_date=birth_date)

    def test_save_profile(self):
        user = self.create_valid_user()
        user.bio = "Hello, my name is Darren."
        user.save()
        self.assertEqual(user.bio, "Hello, my name is Darren.")

    def test_set_gender(self):
        user = self.create_valid_user()
        user.gender = user.Gender.FEMALE
        user.save()
        self.assertEqual(user.gender, "F")

    def test_set_dob_privacy(self):
        user = self.create_valid_user()
        user.birth_date_privacy = "PA"
        user.save()
        self.assertEqual(user.birth_date_privacy, "PA")

    def test_get_links(self):
        user = self.create_valid_user()
        user.links = '''This is line 1
And this is line 2'''
        user.save()
        self.assertEqual(user.get_links(), ["This is line 1", "And this is line 2"])

    def test_get_dob_private(self):
        user = self.create_valid_user()
        user.birth_date = date(2002, 8, 3)
        user.save()
        self.assertFalse(user.get_dob())

    def test_get_dob_public(self):
        user = self.create_valid_user()
        user.birth_date = date(2002, 8, 3)
        user.birth_date_privacy = "PA"
        user.save()
        self.assertEqual(user.get_dob(), "03 Aug 2002")

    def test_get_dob_year(self):
        user = self.create_valid_user()
        user.birth_date = date(2002, 8, 3)
        user.birth_date_privacy = "PY"
        user.save()
        self.assertEqual(user.get_dob(), "2002")

    def test_get_dob_year_month(self):
        user = self.create_valid_user()
        user.birth_date = date(2002, 8, 3)
        user.birth_date_privacy = "PM"
        user.save()
        self.assertEqual(user.get_dob(), "Aug 2002")


class EditProfileTests(TestCase):
    username = "Bilbo"
    password = "swaggins"

    def create_valid_user(self):
        user = User.objects.create_user(self.username, 'bbaggins@theshire.com', self.password,
                                        birth_date=date(2002, 8, 3))
        return user

    def test_change_location(self):
        user = self.create_valid_user()
        self.client.post(reverse("user:login"), {'username': self.username, 'password': self.password})
        response = self.client.post(reverse("user:edit_profile"), {
            'user': user,
            'gender': user.gender,
            'birth_date': user.birth_date,
            'birth_date_privacy': user.birth_date_privacy,
            'location': "The Shire",
            'links': "",
            'bio': "",
        }, follow=True)
        self.assertContains(response, "Profile updated successfully")
        self.assertContains(response, "The Shire")

    def test_invalid_birth_date(self):
        user = self.create_valid_user()
        self.client.post(reverse("user:login"), {'username': self.username, 'password': self.password})
        response = self.client.post(reverse("user:edit_profile"), {
            'user': user,
            'gender': user.gender,
            'birth_date': date.today(),
            'birth_date_privacy': user.birth_date_privacy,
            'location': "",
            'links': "",
            'bio': "",
        }, follow=True)

        self.assertContains(response, "You must be at least 13 years old.")
        self.assertNotEqual(user.birth_date, date.today())

    def test_invalid_gender(self):
        user = self.create_valid_user()
        self.client.post(reverse("user:login"), {'username': self.username, 'password': self.password})
        response = self.client.post(reverse("user:edit_profile"), {
            'user': user,
            'gender': 'X',
            'birth_date': user.birth_date,
            'birth_date_privacy': user.birth_date_privacy,
            'location': "",
            'links': "",
            'bio': "",
        }, follow=True)

        self.assertContains(response, "Select a valid choice. X is not one of the available choices.")
        self.assertNotEqual(user.gender, 'X')


class EditAccountTests(TestCase):
    username = "TestUser"
    password = "APassword"
    birth_date = date(2000, 1, 1)

    def create_valid_user(self):
        user = User.objects.create_user(self.username, 'bbaggins@theshire.com', self.password,
                                        birth_date=self.birth_date)
        self.client.post(reverse("user:login"), {'username': self.username, 'password': self.password})
        return user

    def test_invalid_form(self):
        self.create_valid_user()
        response = self.client.post(reverse("user:edit_account"), {
            'form-type': "invalid_form_type",
        }, follow=True)
        self.assertContains(response, "Invalid form type!")

    def test_change_password(self):
        user = self.create_valid_user()
        new_password = "APassword1"
        response = self.client.post(reverse("user:edit_account"), {
            'user': user,
            'form-type': "password_form",
            'old_password': self.password,
            'new_password1': new_password,
            'new_password2': new_password,
        }, follow=True)
        self.assertContains(response, "Password updated successfully!")
        user = authenticate(username=self.username, password=self.password)
        self.assertIsNone(user)
        user = authenticate(username=self.username, password=new_password)
        self.assertIsNotNone(user)

    def test_delete_account(self):
        user = self.create_valid_user()
        self.assertFalse(user.marked_for_deletion)
        response = self.client.post(reverse("user:delete_account"), {}, follow=True)
        user.refresh_from_db()
        self.assertTrue(user.marked_for_deletion)
        self.assertContains(response, "Account Deletion Request Received")

    def test_cancel_deletion(self):
        user = self.create_valid_user()
        self.client.post(reverse("user:delete_account"))
        user.refresh_from_db()
        self.assertTrue(user.marked_for_deletion)
        response = self.client.post(reverse("user:delete_account"), {}, follow=True)
        user.refresh_from_db()
        self.assertFalse(user.marked_for_deletion)
        self.assertContains(response, "Your account will no longer be deleted!")

    def test_change_username(self):
        user = self.create_valid_user()
        self.client.post(reverse("user:edit_account"), {
            "form-type": "username_form",
            "username": "Jimbo"
        })
        user.refresh_from_db()
        self.assertEqual(user.username, "Jimbo")

    def test_invalid_username(self):
        user = self.create_valid_user()
        self.client.post(reverse("user:edit_account"), {
            "form-type": "username_form",
            "username": "A"
        })
        user.refresh_from_db()
        self.assertNotEqual(user.username, "Jimbo")

    def test_change_email(self):
        user = self.create_valid_user()
        self.client.post(reverse("user:edit_account"), {
            "form-type": "email_form",
            "email": "test@test.com"
        })
        user.refresh_from_db()
        self.assertEqual(user.email, "test@test.com")

    def test_invalid_email(self):
        user = self.create_valid_user()
        self.client.post(reverse("user:edit_account"), {
            "form-type": "email_form",
            "email": "A"
        })
        user.refresh_from_db()
        self.assertNotEqual(user.username, "A")


class TaskTests(TestCase):
    username = "TestUser"
    password = "APassword"
    birth_date = date(2000, 1, 1)

    def create_valid_user(self):
        user = User.objects.create_user(self.username, 'bbaggins@theshire.com', self.password,
                                        birth_date=self.birth_date)
        self.client.post(reverse("user:login"), {'username': self.username, 'password': self.password})
        return user

    def test_delete_none(self):
        user = self.create_valid_user()
        call_command('deleteusers')
        User.objects.get(pk=user.pk)

    def test_delete_marked_account(self):
        user = self.create_valid_user()
        user.marked_for_deletion = True
        user.deletion_date = date.today()
        user.save()
        call_command('deleteusers')
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=user.pk)

    def test_delete_missed_marked_account(self):
        user = self.create_valid_user()
        user.marked_for_deletion = True
        user.deletion_date = date.today() + timedelta(days=-1)
        user.save()
        call_command('deleteusers')
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=user.pk)

    def test_dont_delete_future_marked_account(self):
        user = self.create_valid_user()
        user.marked_for_deletion = True
        user.deletion_date = date.today() + timedelta(days=1)
        user.save()
        call_command('deleteusers')
        User.objects.get(pk=user.pk)

    def test_force_delete_marked_account(self):
        user = self.create_valid_user()
        user.marked_for_deletion = True
        user.save()
        call_command('deleteusers', force=True)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=user.pk)

