from django.core.management.base import BaseCommand, CommandError
from user.models import User
from datetime import date


class Command(BaseCommand):
    help = 'Deletes user accounts scheduled for deletion'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Delete all user accounts marked for deletion - regardless of date'
        )

    def handle(self, *args, **options):
        if options['force']:
            users = User.objects.filter(marked_for_deletion=True)
        else:
            users = User.objects.filter(marked_for_deletion=True).filter(deletion_date__lte=date.today())

        for user in users:
            user.delete()

        self.stdout.write((self.style.SUCCESS('Successfully deleted all accounts marked for deletion!')))
