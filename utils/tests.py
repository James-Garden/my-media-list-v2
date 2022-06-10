from datetime import date
from utils.validators import validate_age, validate_username
from django.core.exceptions import ValidationError
from django.test import TestCase


class ValidatorTests(TestCase):
    def test_valid_username(self):
        self.assertIsNone(validate_username("TestUsername"))

    def test_valid_username_with_special_characters(self):
        self.assertIsNone(validate_username("Test_Username123"))

    def test_invalid_username_no_capital(self):
        with self.assertRaises(ValidationError):
            validate_username("testUsername")

    def test_invalid_username_invalid_char(self):
        with self.assertRaises(ValidationError):
            validate_username("Test-Username")

    def test_valid_dob(self):
        self.assertIsNone(validate_age(date(2002, 8, 3)))

    def test_invalid_dob(self):
        with self.assertRaises(ValidationError):
            validate_age(date.today())

    def test_invalid_dob_too_old(self):
        with self.assertRaises(ValidationError):
            validate_age(date(1900, 1, 1))

    def test_dob_thirteen_years(self):
        valid_birth_date = date.today()
        valid_birth_date = valid_birth_date.replace(year=valid_birth_date.year - 13)
        self.assertIsNone(validate_age(valid_birth_date))
