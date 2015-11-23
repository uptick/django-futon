from django.core.management.base import BaseCommand, CommandError

from futon.models import Token


class Command(BaseCommand):
    help = 'Revoke all access tokens.'

    def handle(self, *args, **options):
        Token.objects.all().delete()
