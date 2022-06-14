from user.models import User
from datetime import date


def delete_marked_accounts():
    users = User.objects.filter(marked_for_deletion=True).filter(deletion_date__lte=date.today())
    for user in users:
        user.delete()
