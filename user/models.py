from datetime import date, timedelta
from utils.validators import validate_age, validate_username
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class BirthDatePrivacy(models.TextChoices):
        PRIVATE = 'PR', _('Private')
        PUBLIC = 'PA', _('Public')
        PUBLIC_YEAR_ONLY = 'PY', _('Public (Year Only)')
        PUBLIC_YEAR_MONTH = 'PM', _('Public (Year and Month Only)')

    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        NON_BINARY = 'N', _('Non-Binary')
        NOT_SPECIFIED = 'P', _('Not Specified')

    username = models.CharField(
        _("username"),
        max_length=20,
        unique=True,
        help_text=_(
            "Required. 2 to 20 characters. Must start with a capital letter, and only contain letters, digits and _"
        ),
        validators=[validate_username],
        error_messages={
            "unique": _("That username is taken.")
        }
    )
    birth_date = models.DateField(validators=[validate_age])
    birth_date_privacy = models.CharField(
        max_length=2,
        choices=BirthDatePrivacy.choices,
        default=BirthDatePrivacy.PRIVATE,
    )
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.NOT_SPECIFIED
    )
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars')
    location = models.CharField(null=True, blank=True, max_length=200)
    bio = models.TextField(null=True, blank=True)
    links = models.TextField(null=True, blank=True)
    marked_for_deletion = models.BooleanField(default=False)
    deletion_date = models.DateField(null=True, blank=True)

    def get_dob(self):
        if self.birth_date_privacy == self.BirthDatePrivacy.PRIVATE:
            return False
        elif self.birth_date_privacy == self.BirthDatePrivacy.PUBLIC:
            return self.birth_date.strftime("%d %b %Y")
        elif self.birth_date_privacy == self.BirthDatePrivacy.PUBLIC_YEAR_ONLY:
            return self.birth_date.strftime("%Y")
        elif self.birth_date_privacy == self.BirthDatePrivacy.PUBLIC_YEAR_MONTH:
            return self.birth_date.strftime("%b %Y")
        raise TypeError("Invalid Privacy Setting!")

    def get_links(self):
        return self.links.split("\n")

    def schedule_deletion(self):
        self.deletion_date = date.today() + timedelta(days=7)
        self.marked_for_deletion = True
        self.save()

    def cancel_deletion(self):
        self.deletion_date = None
        self.marked_for_deletion = False
        self.save()
