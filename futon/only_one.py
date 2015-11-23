import os

from django.conf import settings
import redis
from redis.exceptions import LockError


REDIS_CLIENT = redis.Redis.from_url(settings.REDIS_URL)


class only_one(object):
    """Redis locking mechanism.

    Provides a simple locking mechanism based on Redis, as a context manager.
    Usage is as follows:

    ..code:
      with only_one('unique-key') as lock:
        if not lock:
          return
        some_function()
    """

    def __init__(self, key, timeout=None):
        self.key = key
        self.timeout = timeout

    def __enter__(self):
        self.have_lock = False
        self.lock = REDIS_CLIENT.lock(self.key, timeout=self.timeout)
        self.have_lock = self.lock.acquire(blocking=False)
        return self.have_lock

    def __exit__(self, type, value, tb):
        if self.have_lock:
            try:
                self.lock.release()
            except LockError:
                pass
