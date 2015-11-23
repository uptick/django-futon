from django.core.management.base import BaseCommand, CommandError

from futon.tasks import sync


class Command(BaseCommand):
    help = 'Synchronise across sites.'

    def handle(self, *args, **options):
        sync()
