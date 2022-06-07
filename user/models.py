from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Profile(models.Model):
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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
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
    avatar_url = models.URLField(null=True, blank=True)
    location = models.CharField(null=True, blank=True, max_length=200)
    bio = models.TextField(null=True, blank=True)
    links = models.TextField(null=True, blank=True)

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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
