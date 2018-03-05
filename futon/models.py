from django.db import models


class Site(models.Model):
    """A destination site.

    Don't use Django sites. It's a pain in the ass.
    """

    name = models.CharField(max_length=200)
    domain = models.URLField()

    def __str__(self):
        return self.name


class Token(models.Model):
    """An authorization token.

    Once the application has been logged in we need to store the token
    persistently. When the token expires we replace it in the database.

    :site: the site with which the token is associated
    :token: the authorization token
    """

    site = models.ForeignKey(Site, related_name='+', on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __str__(self):
        n_chars = len(self.token)
        n_vis = 0 if (n_chars < 5) else 5
        return self.token[:n_vis] + '*' * (n_chars - n_vis)
