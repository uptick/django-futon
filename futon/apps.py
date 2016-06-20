from datetime import timedelta

import django_rq
from django.apps import AppConfig
from django.utils import timezone


class FutonConfig(AppConfig):
    name = 'futon'
    verbose_name = 'Futon'

    def ready(self):

        # Schedule repeating invoices.
        from .resource import sync
        scheduler = django_rq.get_scheduler('default')
        jobs = scheduler.get_jobs()
        func = sync

        # Remove any scheduled jobs corresponding to this function.
        [scheduler.cancel(x) for x in jobs if x.func == func]

        # Schedule to run every ten minutes. The repeating invoices will only
        # launch daily, but we should be checking for changes more often.
        due = timezone.now() + timedelta(minutes=3)
        scheduler.schedule(due, func, interval=10*60)
