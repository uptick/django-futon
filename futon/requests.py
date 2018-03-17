import logging
import os
import requests
import six
import threading
import urllib.parse

from requests_oauthlib import OAuth2Session

from django.conf import settings

from .credentials import get_credentials
from .models import Site, Token

__all__ = ['fetch', 'create', 'update']


logger = logging.getLogger(__name__)
lock = threading.Lock()


class AuthenticationError(Exception):
    pass


def make_site(site, name=None):
    if isinstance(site, six.string_types):
        if not isinstance(name, six.string_types):
            raise Exception('Must provide a name in addition to a domain.')
        site, created = Site.objects.get_or_create(domain=site, name=name)
    return site


def make_url(site, path):
    """Construct an URL from a path.

    For convenience we let the user pass in just a path. This function tries to
    construct a fully qualified URL using settings.

    :site: the site to append patht o
    :path: the path to convert to an URL
    """
    if not isinstance(site, six.string_types):
        site = site.domain
    return urllib.parse.urljoin(site, path)


def get_token(site, client_id, force=False):
    with lock:
        return _get_token(site, client_id, force=force)


def _get_token(site, client_id, force=False):

    # request_oauthlib won't let us use http, like we need to in debug mode. Setting
    # this value gets around that.
    if settings.DEBUG:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    if not force:
        try:
            return Token.objects.get(site=site).token
        except (Token.DoesNotExist, Token.MultipleObjectsReturned):
            pass

    logger.debug('Requesting a new token.')

    client_secret = settings.SECRET_KEY
    username, password = get_credentials(site)

    # Client key and secret
#    secret = client_id + ':' + client_secret
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
    }
    url = make_url(site, '/api/oauth2/token/')

    response = requests.post(url, data=data, auth=(client_id, client_secret))
    if response.status_code != 200:
        raise AuthenticationError('Failed to authenticate: %s' % response.content)

    response_data = response.json()
    token = response_data['access_token']
    Token.objects.filter(site=site).delete()
    Token.objects.create(site=site, token=token)
    return token


def authorise(site, force=False):
    client_id = settings.CLIENT_ID
    token = get_token(site, client_id, force)
    token = {
        'access_token': token,
        'token': token,
    }
    hub = OAuth2Session(client_id, token=token)
    return hub


def execute(site, method, url, *args, **kwargs):
    site = make_site(site, kwargs.pop('name', None))
    reauth = kwargs.pop('reauth', False)
    hub = authorise(site, reauth)
    call = getattr(hub, method)

    # Due to changes to the Oauth API we need to change
    # any data requests to json.
    data = kwargs.pop('data', None)
    if data is not None:
        kwargs['json'] = data

    response = call(url, *args, **kwargs)

    if (response.status_code == 403 or response.status_code == 401) and not reauth:
        return execute(site, method, url, *args, reauth=True, **kwargs)

    return response


def fetch(site, path, *args, **kwargs):
    """GET data from the server.

    Performs a GET from the server, authenticating the application if necessary.

    :path: the endpoint to access
    """
    url = make_url(site, path)
    return execute(site, 'get', url, **kwargs)


def create(site, path, data, *args, **kwargs):
    """POST data to the server.

    Performs a POST to the server, authenticating the application if necessary.

    :path: the endpoint to access
    :data: the data to send
    """
    url = make_url(site, path)
    return execute(site, 'post', url, data=data, **kwargs)


def update(site, path, data, *args, **kwargs):
    """PATCH data to the server.

    Performs a PATCH to the server, authenticating the application if necessary.

    :path: the endpoint to access
    :data: the data to send
    """
    url = make_url(site, path)
    return execute(site, 'patch', url, data=data, **kwargs)


def upsert(site, path, data, *args, **kwargs):
    """PUT data to the server.

    Performs a PUT to the server, authenticating the application if necessary.

    :path: the endpoint to access
    :data: the data to send
    """
    url = make_url(site, path)
    return execute(site, 'put', url, data=data, **kwargs)
