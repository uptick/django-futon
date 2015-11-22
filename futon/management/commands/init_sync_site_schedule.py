from django.core.management.base import BaseCommand, CommandError

from djcelery.models import PeriodicTask, IntervalSchedule

from abas.apps.futon.tasks import sync


class Command(BaseCommand):
    help = 'Initialise site synchronisation schedule.'

    def handle(self, *args, **options):
        try:
            ptask = PeriodicTask.objects.get(name='futon-schedule')
        except PeriodicTask.DoesNotExist:
            ptask = None
        if not ptask:
            sched, created = IntervalSchedule.objects.get_or_create(period='seconds', every=30)
            ptask = PeriodicTask.objects.create(name='futon-schedule', task=sync.name, interval=sched)
