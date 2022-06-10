from datetime import datetime, date
from re import match
from django.core.exceptions import ValidationError


def validate_username(value):
    if not match(r"^[A-Z][\w_]+$", str(value)):
        raise ValidationError("Username must start with a capital letter and be alphanumeric.")


def validate_age(value):
    valid_birth_date = datetime.now()
    valid_birth_date = valid_birth_date.replace(year=valid_birth_date.year - 13).date()
    if value.year < 1903:
        raise ValidationError("Please enter a valid birth year")
    if value > valid_birth_date:
        raise ValidationError("You must be at least 13 years old.")
