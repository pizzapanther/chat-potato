import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

import jwt


class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  version = models.PositiveIntegerField(default=0)

  @property
  def jwt(self):
    exp = timezone.now() + datetime.timedelta(days=14)
    payload = {"user": self.user.id, "version": self.version, "exp": exp}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return {'token': token, 'expires': exp.isoformat()}

  @property
  def temp_token(self):
    exp = timezone.now() + datetime.timedelta(minutes=5)
    payload = {"user": self.user.id, "version": self.version, "exp": exp}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
