from django.db import models
from django.contrib.sites.models import Site


class Token(models.Model):
    """An authorization token.

    Once the application has been logged in we need to store the token persistently.
    When the token expires we replace it in the database.

    :site: the site with which the token is associated
    :token: the authorization token
    """

    site  = models.ForeignKey(Site, related_name='+')
    token = models.CharField(max_length=255)

    def __str__(self):
        n_chars = len(self.token)
        n_vis = 0 if (n_chars < 5) else 5
        return self.token[:n_vis] + '*'*(n_chars - n_vis)
