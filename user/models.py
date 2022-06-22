from datetime import date, timedelta
from utils.validators import validate_age, validate_username
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


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
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.jpg')
    location = models.CharField(null=True, blank=True, max_length=100)
    bio = models.TextField(null=True, blank=True)
    links = models.TextField(null=True, blank=True)
    marked_for_deletion = models.BooleanField(default=False)
    deletion_date = models.DateField(null=True, blank=True)
    last_online = models.DateTimeField(default=now)
    friends = models.ManyToManyField("User", blank=True)

    def get_dob(self):
        if self.birth_date_privacy == self.BirthDatePrivacy.PRIVATE:
            return False
        elif self.birth_date_privacy == self.BirthDatePrivacy.PUBLIC:
            return self.birth_date.strftime("%d %b, %Y")
        elif self.birth_date_privacy == self.BirthDatePrivacy.PUBLIC_YEAR_ONLY:
            return self.birth_date.strftime("%Y")
        elif self.birth_date_privacy == self.BirthDatePrivacy.PUBLIC_YEAR_MONTH:
            return self.birth_date.strftime("%b %Y")
        raise TypeError("Invalid Privacy Setting!")

    def get_links(self) -> [str]:
        return self.links.split("\n")

    def get_last_online(self) -> str:
        delta = now() - self.last_online
        if delta.days == 0:
            if delta.seconds < 300:
                return "Now"
            elif delta.seconds < 3600:
                return f"{delta.seconds // 60} minutes ago"
            elif delta.seconds < 7200:
                return "1 hour ago"
            else:
                return f"{delta.seconds // 3600} hours ago"
        else:
            if delta.days == 1:
                return "Yesterday"
            elif delta.days < 7:
                return f"{delta.days} days ago"
            elif delta.days == 7:
                return "Last week"
            elif delta.days < 30:
                return f"{delta.days} weeks ago"
            elif delta.days < 365:
                return f"{delta.days // 30} months ago"
            elif delta.days < 730:
                return "Last year"
            else:
                return f"{delta.days // 365} years ago"

    def get_date_joined(self) -> str:
        return self.date_joined.strftime("%d %b, %Y")

    def get_gender(self):
        if self.gender == 'P':
            return None
        for pair in self.Gender.choices:
            if pair[0] == self.gender:
                return pair[1]

    def schedule_deletion(self) -> None:
        self.deletion_date = date.today() + timedelta(days=7)
        self.marked_for_deletion = True
        self.save()

    def cancel_deletion(self) -> None:
        self.deletion_date = None
        self.marked_for_deletion = False
        self.save()

    def unfriend(self, friend: 'User'):
        self.friends.remove(friend)
        friend.friends.remove(self)

    def send_friend_request(self, recipient: 'User'):
        FriendRequest.objects.create(from_user=self, to_user=recipient)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

    def accept(self) -> None:
        self.from_user.friends.add(self.to_user)  # Add recipient to senders friends
        self.to_user.friends.add(self.from_user)  # Add sender to recipients friends
        self.delete()  # Delete the request

    def deny(self) -> None:
        self.delete()  # Delete the request
