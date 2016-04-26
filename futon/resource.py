import logging

from django.db import models
from django.contrib.sites.models import Site

from .requests import fetch, AuthenticationError


logger = logging.getLogger(__name__)


class BadResourceError(Exception):
    pass


class BadSyncError(Exception):
    pass


class Resource(object):
    """Define mappings from external APIs to local models.
    """
    model = None
    serializer = None
    mapping = {}
    endpoint = None
    domain = None
    primary_key = 'id'

    @classmethod
    def _validate(self):
        for attr in ['model', 'serializer', 'mapping', 'endpoint']:
            if getattr(self, attr, None) is None:
                raise BadResourceError('`{}` must be specified'.format(attr))
        for k, v in self.mapping.items():
            try:
                self.model._meta.get_field(k)
            except models.FieldDoesNotExist:
                raise BadResourceError('Model `{}` does not have field `{}`'.format(
                    self.model.__name__, k
                ))

    @classmethod
    def sync(self, site=None):
        logger.info('Synchronising resource')

        self._validate()
        if not site:
            if self.domain is None:
                raise BadSyncError('Must provide a site or specify `domain`')
            try:
                site = Site.objects.get(domain=self.domain)
            except Site.DoesNotExist:
                raise BadSyncError('Unable to find a site with domain `{}`'.format(self.domain))

        logger.info('Fetching resource from {}{}'.format(site, self.endpoint))
        data = fetch(site, self.endpoint)['results']

        pks = set()
        pk = self.primary_key
        for inst in data:
            mapped_inst = self._map_data(inst)

            try:
                obj = self.model.objects.get(id=inst[pk])
            except self.model.DoesNotExist:
                obj = None

            serializer = self.serializer(data=mapped_inst)
            serializer.is_valid(raise_exception=True)
            if not obj:
                serializer.validated_data[pk] = inst[pk]
            obj = serializer.save()

            if obj.id != inst[pk]:
                raise BadSyncError('PKs don\'t match: %d and %d'%(obj.id, inst[pk]))

            logger.info('Fetched from %s: %s'%(self.endpoint, obj))
            pks.add(inst[pk])

        for obj in list(self.model.objects.all()):
            if obj.pk not in pks:
                obj.delete()
                logger.info('Deleted from %s: %s'%(self.endpoint, obj))

    @classmethod
    def _map_data(self, data):
        mapped_data = {}
        for k, v in self.mapping.items():
            mapped_data[v] = data[k]
        return mapped_data
