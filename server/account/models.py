from django.conf import settings
from django.db import models

import jwt


class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  version = models.PositiveIntegerField(default=0)

  @property
  def jwt(self):
    return {}

  @property
  def temp_token(self):
    payload = {"user": self.user.id, "version": self.version}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
