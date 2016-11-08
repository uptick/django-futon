import importlib
import logging

from django.conf import settings
from requests.exceptions import ConnectionError

from .requests import fetch, AuthenticationError
from .models import Site


logger = logging.getLogger(__name__)


class SiteSyncError(Exception):
    pass


def sync():
    logger.debug('Beginning futon site sync.')
    for site_name in settings.SYNC_SITES.keys():
        try:
            site = Site.objects.get(name__iexact=site_name)
        except Site.DoesNotExist:
            logger.error('Site does not exist: %s'%site_name)
            continue
        try:
            sync_site(site)
        except ConnectionError:
            logger.error('Failed to connect to site: %s'%site)
        except AuthenticationError:
            logger.error('Failed to authenticate to site: %s'%site)
    logger.debug('Finished futon site sync.')


def sync_site(site):
    site_name = site.name.lower()
    for method, viewset_descs in settings.SYNC_SITES.get(site_name, {}).items():

        if method == 'pull':
            sync_func = pull_viewset
        else:
            sync_func = None

        for viewset_desc, endpoint in viewset_descs:
            ii = viewset_desc.rfind('.')
            pkg, name = viewset_desc[:ii], viewset_desc[ii + 1:]
            viewset = getattr(importlib.import_module(pkg), name)
            sync_func(site, viewset(), endpoint)


def pull_viewset(site, viewset, endpoint):
    viewset.request = None
    viewset.format_kwarg = viewset.get_format_suffix()
    model = viewset.queryset.model

    data = fetch(site, endpoint)['results']
    pks = set()
    for inst in data:

        try:
            obj = model.objects.get(id=inst['id'])
        except model.DoesNotExist:
            obj = None

        serializer = viewset.get_serializer(obj, data=inst)
        serializer.is_valid(raise_exception=True)
        if not obj:
            serializer.validated_data['id'] = inst['id']
        obj = serializer.save()

        if obj.id != inst['id']:
            raise SiteSyncError(site, 'PKs don\'t match: %d and %d'%(obj.id, inst['id']))

        logger.debug('Fetched from %s: %s'%(endpoint, obj))

        pks.add(inst['id'])

    for obj in list(model.objects.all()):
        if obj.pk not in pks:
            logger.debug('Deleted from %s: %s'%(endpoint, obj))
            obj.delete()
