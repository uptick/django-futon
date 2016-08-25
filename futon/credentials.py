import os

from django.conf import settings

__all__ = ['get_credentials']


def _get(name, ext):
    return settings.FUTON_SITES.get(name.lower(), {}).get(
        ext,
        getattr(
            settings, 'FUTON_DEFAULT_' + ext.upper(),
            os.environ.get(
                name.upper() + '_' + ext.upper(),
                os.environ.get('FUTON_DEFAULT_' + ext.upper(), None))))


def get_credentials(site):
    name = site.name
    return _get(name, 'username'), _get(name, 'password')
