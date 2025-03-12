from django.db import models
from django.contrib.auth.models import User


class SpotifyToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    token_type = models.CharField(max_length=50)
    expires_in = models.DateTimeField()


class SpotifyUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    display_name = models.CharField(max_length=50)
    spotify_id = models.CharField(max_length=75)
    spotify_uri = models.CharField(max_length=100)
    profile_image = models.URLField(max_length=200, null=True)

