from django.core.management.base import BaseCommand, CommandError

from futon.tasks import sync, sync_site


class Command(BaseCommand):
    help = 'Synchronise across sites.'

    def add_arguments(self, parser):
        parser.add_arguments('site', help='individual site to sync')

    def handle(self, *args, **options):
        site = options.get('site', None)
        if site:
            sync_site(site)
        else:
            sync()
