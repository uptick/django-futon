from django.core.management.base import BaseCommand, CommandError

from djcelery.models import PeriodicTask, IntervalSchedule

from futon.tasks import sync


class Command(BaseCommand):
    help = 'Initialise site synchronisation schedule.'

    def handle(self, *args, **options):
        PeriodicTask.objects.filter(name='futon-schedule').delete()
        sched, created = IntervalSchedule.objects.get_or_create(period='seconds', every=30)
        PeriodicTask.objects.create(name='futon-schedule', task=sync.name, interval=sched)
